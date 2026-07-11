from datetime import datetime
from flask import Blueprint, request
from flask_restful import Api, Resource
from werkzeug.security import generate_password_hash
from application.models import db, User, Trek, Booking
from application.routes.utils import role_required, serialize_user, serialize_trek, serialize_booking
from application.extensions import cache

admin = Blueprint("admin", __name__, url_prefix="/admin")
admin_api = Api(admin)


class AdminDashboard(Resource):
    @role_required("admin")
    def get(self):
        total_users = User.query.filter_by(role="user").count()
        total_staff = User.query.filter_by(role="staff").count()
        total_treks = Trek.query.count()
        total_bookings = Booking.query.count()
        pending_staff = User.query.filter_by(
            role="staff",
            status="pending"
        ).count()

        # Fetch popular treks (top 5 by booking count)
        popular_treks_query = db.session.query(
            Trek.name, db.func.count(Booking.id).label("booking_count")
        ).join(Booking, Trek.id == Booking.trek_id).group_by(Trek.id).order_by(db.func.count(Booking.id).desc()).limit(5).all()
        popular_treks = [{"name": name, "bookings": count} for name, count in popular_treks_query]

        # Fetch user participation by booking status
        participation_query = db.session.query(
            Booking.status, db.func.count(Booking.id)
        ).group_by(Booking.status).all()
        participation = {status: count for status, count in participation_query}

        return {
            "total_users": total_users,
            "total_staff": total_staff,
            "total_treks": total_treks,
            "total_bookings": total_bookings,
            "pending_staff": pending_staff,
            "popular_treks": popular_treks,
            "participation": participation
        }, 200


class AdminUsersList(Resource):
    @role_required("admin")
    def get(self):
        search = request.args.get("search", "")
        if search:
            users = User.query.filter(
                User.role == "user",
                User.name.contains(search)
            ).all()
        else:
            users = User.query.filter_by(role="user").all()
        return [serialize_user(u) for u in users], 200


class AdminBlacklistUser(Resource):
    @role_required("admin")
    def post(self, id):
        user = User.query.get_or_404(id)
        user.status = "blacklisted"
        db.session.commit()
        return {"message": "User blacklisted."}, 200


class AdminUnblacklistUser(Resource):
    @role_required("admin")
    def post(self, id):
        user = User.query.get_or_404(id)
        user.status = "approved"
        db.session.commit()
        return {"message": "User restored."}, 200


class AdminStaffList(Resource):
    @role_required("admin")
    def get(self):
        search = request.args.get("search", "")
        if search:
            staff = User.query.filter(
                User.role == "staff",
                User.name.contains(search)
            ).all()
        else:
            staff = User.query.filter_by(role="staff").all()
        return [serialize_user(s) for s in staff], 200


class AdminApproveStaff(Resource):
    @role_required("admin")
    def post(self, id):
        staff = User.query.get_or_404(id)
        staff.status = "approved"
        db.session.commit()
        return {"message": "Staff approved successfully."}, 200


class AdminBlacklistStaff(Resource):
    @role_required("admin")
    def post(self, id):
        staff = User.query.get_or_404(id)
        staff.status = "blacklisted"
        db.session.commit()
        return {"message": "Staff blacklisted."}, 200


class AdminUnblacklistStaff(Resource):
    @role_required("admin")
    def post(self, id):
        staff = User.query.get_or_404(id)
        staff.status = "approved"
        db.session.commit()
        return {"message": "Staff restored successfully."}, 200


class AdminAddStaff(Resource):
    @role_required("admin")
    def post(self):
        data = request.get_json(silent=True) or {}
        username = data.get("username", "").strip()
        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        phone = data.get("phone", "").strip()
        password = data.get("password", "")

        if not username or not name or not email or not password:
            return {"message": "Please fill all required fields."}, 400

        if User.query.filter_by(username=username).first():
            return {"message": "Username already exists."}, 400

        if User.query.filter_by(email=email).first():
            return {"message": "Email already registered."}, 400

        new_staff = User(
            username=username,
            name=name,
            email=email,
            phone=phone,
            password=generate_password_hash(password),
            role="staff",
            status="approved"
        )
        db.session.add(new_staff)
        db.session.commit()
        return {"message": "Staff added successfully.", "staff": serialize_user(new_staff)}, 201


class AdminTreksList(Resource):
    @role_required("admin")
    def get(self):
        search = request.args.get("search", "")
        if search:
            treks = Trek.query.filter(
                Trek.name.contains(search)
            ).all()
        else:
            treks = Trek.query.all()
        return [serialize_trek(t) for t in treks], 200


class AdminAddTrek(Resource):
    @role_required("admin")
    def post(self):
        data = request.get_json(silent=True) or {}
        try:
            start_date = datetime.strptime(data.get("start_date"), "%Y-%m-%d").date()
            end_date = datetime.strptime(data.get("end_date"), "%Y-%m-%d").date()
        except (ValueError, TypeError):
            return {"message": "Invalid date format. Use YYYY-MM-DD."}, 400

        try:
            duration = int(data.get("duration", 0))
            total_slots = int(data.get("total_slots", 0))
            available_slots = int(data.get("available_slots", total_slots))
        except (ValueError, TypeError):
            return {"message": "Duration and slots must be integers."}, 400

        trek = Trek(
            name=data.get("name"),
            location=data.get("location"),
            difficulty=data.get("difficulty"),
            duration=duration,
            total_slots=total_slots,
            available_slots=available_slots,
            start_date=start_date,
            end_date=end_date,
            description=data.get("description")
        )
        db.session.add(trek)
        db.session.commit()
        cache.clear()
        return {"message": "Trek added successfully.", "trek": serialize_trek(trek)}, 201


class AdminAssignStaff(Resource):
    @role_required("admin")
    def post(self, id):
        trek = Trek.query.get_or_404(id)
        data = request.get_json(silent=True) or {}
        staff_id = data.get("staff_id")

        if staff_id:
            try:
                staff_id_int = int(staff_id)
                staff_user = User.query.filter_by(id=staff_id_int, role="staff", status="approved").first()
                if not staff_user:
                    return {"message": "Staff member not found or not approved."}, 404
                trek.assigned_staff = staff_id_int
            except (ValueError, TypeError):
                return {"message": "Invalid staff ID."}, 400
        else:
            trek.assigned_staff = None

        db.session.commit()
        cache.clear()
        return {"message": "Staff assigned successfully."}, 200


class AdminEditTrek(Resource):
    @role_required("admin")
    def put(self, id):
        trek = Trek.query.get_or_404(id)
        data = request.get_json(silent=True) or {}
        
        try:
            if "start_date" in data:
                trek.start_date = datetime.strptime(data["start_date"], "%Y-%m-%d").date()
            if "end_date" in data:
                trek.end_date = datetime.strptime(data["end_date"], "%Y-%m-%d").date()
        except (ValueError, TypeError):
            return {"message": "Invalid date format. Use YYYY-MM-DD."}, 400

        if "name" in data:
            trek.name = data["name"]
        if "location" in data:
            trek.location = data["location"]
        if "difficulty" in data:
            trek.difficulty = data["difficulty"]
        if "duration" in data:
            try:
                trek.duration = int(data["duration"])
            except (ValueError, TypeError):
                return {"message": "Duration must be an integer."}, 400
        if "total_slots" in data:
            try:
                trek.total_slots = int(data["total_slots"])
            except (ValueError, TypeError):
                return {"message": "Total slots must be an integer."}, 400
        if "available_slots" in data:
            try:
                trek.available_slots = int(data["available_slots"])
            except (ValueError, TypeError):
                return {"message": "Available slots must be an integer."}, 400
        if "description" in data:
            trek.description = data["description"]

        db.session.commit()
        cache.clear()
        return {"message": "Trek updated successfully."}, 200


class AdminDeleteTrek(Resource):
    @role_required("admin")
    def delete(self, id):
        trek = Trek.query.get_or_404(id)
        trek.is_deleted = True
        db.session.commit()
        cache.clear()
        return {"message": "Trek removed."}, 200


class AdminRestoreTrek(Resource):
    @role_required("admin")
    def post(self, id):
        trek = Trek.query.get_or_404(id)
        trek.is_deleted = False
        db.session.commit()
        cache.clear()
        return {"message": "Trek restored."}, 200


class AdminBookingsList(Resource):
    @role_required("admin")
    def get(self):
        search = request.args.get("search", "")
        if search:
            bookings = Booking.query.join(User).join(Trek).filter(
                (User.name.contains(search)) |
                (Trek.name.contains(search))
            ).all()
        else:
            bookings = Booking.query.all()
        return [serialize_booking(b) for b in bookings], 200


admin_api.add_resource(AdminDashboard, "/dashboard")
admin_api.add_resource(AdminUsersList, "/users")
admin_api.add_resource(AdminBlacklistUser, "/users/blacklist/<int:id>")
admin_api.add_resource(AdminUnblacklistUser, "/users/unblacklist/<int:id>")
admin_api.add_resource(AdminStaffList, "/staff")
admin_api.add_resource(AdminAddStaff, "/staff/add")
admin_api.add_resource(AdminApproveStaff, "/staff/approve/<int:id>")
admin_api.add_resource(AdminBlacklistStaff, "/staff/blacklist/<int:id>")
admin_api.add_resource(AdminUnblacklistStaff, "/staff/unblacklist/<int:id>")
admin_api.add_resource(AdminTreksList, "/treks")
admin_api.add_resource(AdminAddTrek, "/treks/add")
admin_api.add_resource(AdminAssignStaff, "/treks/assign/<int:id>")
admin_api.add_resource(AdminEditTrek, "/treks/edit/<int:id>")
admin_api.add_resource(AdminDeleteTrek, "/treks/delete/<int:id>")
admin_api.add_resource(AdminRestoreTrek, "/treks/restore/<int:id>")
admin_api.add_resource(AdminBookingsList, "/bookings")
