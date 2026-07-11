from flask import Blueprint
from flask_restful import Api, Resource
from application.models import User, Trek, Booking
from application.routes.utils import serialize_trek, serialize_user, serialize_booking
from application.extensions import cache

api = Blueprint("api", __name__, url_prefix="/api")
api_api = Api(api)


class APITreks(Resource):
    @cache.cached(timeout=60)
    def get(self):
        treks = Trek.query.all()
        return [serialize_trek(t) for t in treks], 200


class APITrek(Resource):
    def get(self, id):
        trek = Trek.query.get_or_404(id)
        return serialize_trek(trek), 200


class APIUsers(Resource):
    def get(self):
        users = User.query.filter_by(role="user").all()
        return [serialize_user(u) for u in users], 200


class APIStaff(Resource):
    def get(self):
        staff = User.query.filter_by(role="staff").all()
        return [serialize_user(s) for s in staff], 200


class APIBookings(Resource):
    def get(self):
        bookings = Booking.query.all()
        return [serialize_booking(b) for b in bookings], 200


api_api.add_resource(APITreks, "/treks")
api_api.add_resource(APITrek, "/treks/<int:id>")
api_api.add_resource(APIUsers, "/users")
api_api.add_resource(APIStaff, "/staff")
api_api.add_resource(APIBookings, "/bookings")
