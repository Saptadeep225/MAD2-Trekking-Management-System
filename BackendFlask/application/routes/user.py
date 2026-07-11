import os
import json
from datetime import datetime
from flask import Blueprint, request, current_app
from flask_restful import Api, Resource
from flask_jwt_extended import current_user
from application.models import db, Trek, Booking, User
from application.routes.utils import role_required, serialize_trek, serialize_booking, serialize_user
from application.extensions import cache

user = Blueprint("user", __name__, url_prefix="/user")
user_api = Api(user)


class UserDashboard(Resource):
    @role_required("user")
    def get(self):
        total_bookings = Booking.query.filter_by(
            user_id=current_user.id
        ).count()
        upcoming = Booking.query.filter_by(
            user_id=current_user.id,
            status="Booked"
        ).count()
        completed = Booking.query.filter_by(
            user_id=current_user.id,
            status="Completed"
        ).count()

        return {
            "total_bookings": total_bookings,
            "upcoming": upcoming,
            "completed": completed
        }, 200


class UserTreksList(Resource):
    @role_required("user")
    @cache.cached(timeout=60, query_string=True)
    def get(self):
        search = request.args.get("search", "")
        difficulty = request.args.get("difficulty", "")
        location = request.args.get("location", "")
        query = Trek.query.filter_by(status="Open", is_deleted=False)

        if search:
            query = query.filter(
                Trek.name.contains(search)
            )
        if difficulty:
            query = query.filter_by(
                difficulty=difficulty
            )
        if location:
            query = query.filter(
                Trek.location.contains(location)
            )

        treks = query.all()
        return [serialize_trek(t) for t in treks], 200


class UserBookTrek(Resource):
    @role_required("user")
    def post(self, id):
        trek = Trek.query.get_or_404(id)
        if trek.is_deleted:
            return {"message": "This trek is no longer available."}, 404
        if trek.available_slots <= 0:
            return {"message": "No slots available."}, 400

        existing = Booking.query.filter_by(
            user_id=current_user.id,
            trek_id=trek.id
        ).first()

        if existing:
            return {"message": "You have already booked this trek."}, 400

        booking = Booking(
            user_id=current_user.id,
            trek_id=trek.id,
            booking_date=datetime.now(),
            number_of_people=1,
            status="Booked"
        )
        trek.available_slots -= 1
        db.session.add(booking)
        db.session.commit()
        cache.clear()

        return {
            "message": "Booking Successful!",
            "booking": serialize_booking(booking)
        }, 201


class UserBookingsList(Resource):
    @role_required("user")
    def get(self):
        bookings = Booking.query.filter_by(
            user_id=current_user.id
        ).all()
        return [serialize_booking(b) for b in bookings], 200


class UserProfile(Resource):
    @role_required("user")
    def get(self):
        return serialize_user(current_user), 200

    @role_required("user")
    def put(self):
        data = request.get_json(silent=True) or {}
        if "name" in data:
            current_user.name = data["name"]
        if "phone" in data:
            current_user.phone = data["phone"]
        if "email" in data:
            email = data["email"]
            existing_user = User.query.filter_by(email=email).first()
            if existing_user and existing_user.id != current_user.id:
                return {"message": "Email already registered by another account."}, 400
            current_user.email = email

        db.session.commit()
        return {
            "message": "Profile Updated!",
            "user": serialize_user(current_user)
        }, 200


class UserCancelBooking(Resource):
    @role_required("user")
    def post(self, id):
        booking = Booking.query.filter_by(id=id, user_id=current_user.id).first()
        if not booking:
            return {"message": "Booking not found."}, 404
        if booking.status == "Cancelled":
            return {"message": "Booking is already cancelled."}, 400

        booking.status = "Cancelled"
        trek = booking.trek
        if trek:
            trek.available_slots += 1
        db.session.commit()
        cache.clear()
        return {"message": "Booking cancelled successfully.", "booking": serialize_booking(booking)}, 200


class UserExportHistory(Resource):
    @role_required("user")
    def post(self):
        from application.tasks import export_bookings_csv
        try:
            export_bookings_csv.delay(current_user.id, current_user.username)
            return {"message": "Export task triggered! You will receive a notification when complete."}, 202
        except Exception:
            # Fallback to local thread if Celery/Redis is offline
            import threading
            thread = threading.Thread(
                target=export_bookings_csv,
                args=(current_user.id, current_user.username)
            )
            thread.start()
            return {"message": "Export task started in local thread (Redis is offline). You will receive a notification when complete."}, 202


class UserNotificationsList(Resource):
    @role_required("user")
    def get(self):
        filepath = os.path.join(current_app.root_path, "instance", "notifications", f"{current_user.id}.json")
        if not os.path.exists(filepath):
            return [], 200
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data, 200
        except Exception:
            return [], 200


class UserNotificationsClear(Resource):
    @role_required("user")
    def post(self):
        filepath = os.path.join(current_app.root_path, "instance", "notifications", f"{current_user.id}.json")
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except Exception:
                pass
        return {"message": "Notifications cleared."}, 200


user_api.add_resource(UserDashboard, "/dashboard")
user_api.add_resource(UserTreksList, "/treks")
user_api.add_resource(UserBookTrek, "/book/<int:id>")
user_api.add_resource(UserBookingsList, "/bookings")
user_api.add_resource(UserProfile, "/profile")
user_api.add_resource(UserCancelBooking, "/bookings/cancel/<int:id>")
user_api.add_resource(UserExportHistory, "/export")
user_api.add_resource(UserNotificationsList, "/notifications")
user_api.add_resource(UserNotificationsClear, "/notifications/clear")
