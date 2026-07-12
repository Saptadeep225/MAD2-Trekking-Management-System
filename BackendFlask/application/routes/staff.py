from flask import Blueprint, request
from flask_restful import Api, Resource
from flask_jwt_extended import current_user
from application.models import db, Trek, Booking
from application.routes.utils import role_required, serialize_trek, serialize_booking
from application.extensions import cache

staff = Blueprint("staff", __name__, url_prefix="/staff")
staff_api = Api(staff)


class StaffDashboard(Resource):
    @role_required("staff")
    def get(self):
        assigned_treks = Trek.query.filter_by(
            assigned_staff=current_user.id
        ).count()

        total_participants = Booking.query.join(Trek).filter(
            Trek.assigned_staff == current_user.id
        ).count()

        return {
            "assigned_treks": assigned_treks,
            "total_participants": total_participants
        }, 200


class StaffAssignedTreks(Resource):
    @role_required("staff")
    def get(self):
        treks = Trek.query.filter_by(
            assigned_staff=current_user.id
        ).all()
        return [serialize_trek(t) for t in treks], 200


class StaffUpdateTrek(Resource):
    @role_required("staff")
    def get(self, id):
        trek = Trek.query.get_or_404(id)
        return serialize_trek(trek), 200

    @role_required("staff")
    def put(self, id):
        trek = Trek.query.get_or_404(id)
        if trek.assigned_staff != current_user.id:
            return {"message": "Access Denied! You are not assigned to this trek."}, 403

        data = request.get_json(silent=True) or {}
        if "available_slots" in data:
            try:
                trek.available_slots = int(data["available_slots"])
            except (ValueError, TypeError):
                return {"message": "available_slots must be an integer."}, 400
        if "status" in data:
            status = data["status"]
            trek.status = status
            if status == "Completed":
                Booking.query.filter_by(trek_id=trek.id, status="Booked").update({"status": "Completed"})

        db.session.commit()
        cache.clear()
        return {"message": "Trek updated successfully.", "trek": serialize_trek(trek)}, 200


class StaffTrekParticipants(Resource):
    @role_required("staff")
    def get(self, id):
        trek = Trek.query.get_or_404(id)
        if trek.assigned_staff != current_user.id:
            return {"message": "Access Denied! You are not assigned to this trek."}, 403

        bookings = Booking.query.filter_by(
            trek_id=id
        ).all()
        return [serialize_booking(b) for b in bookings], 200


staff_api.add_resource(StaffDashboard, "/dashboard")
staff_api.add_resource(StaffAssignedTreks, "/treks")
staff_api.add_resource(StaffUpdateTrek, "/treks/update/<int:id>")
staff_api.add_resource(StaffTrekParticipants, "/participants/<int:id>")
