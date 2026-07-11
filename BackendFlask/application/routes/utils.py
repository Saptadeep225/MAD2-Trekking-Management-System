from functools import wraps
from flask_jwt_extended import jwt_required, current_user


def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            if not current_user:
                return {"message": "User not found."}, 404
            if current_user.status == "blacklisted":
                return {"message": "Your account has been blacklisted by the administrator."}, 403
            if current_user.role != role:
                return {"message": f"Access Denied! {role.capitalize()} role required."}, 403
            if role == "staff" and current_user.status != "approved":
                return {"message": "Your account is awaiting admin approval."}, 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper


def serialize_user(user):
    if not user:
        return None
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "name": user.name,
        "phone": user.phone,
        "role": user.role,
        "status": user.status
    }


def serialize_trek(trek):
    if not trek:
        return None
    return {
        "id": trek.id,
        "name": trek.name,
        "location": trek.location,
        "difficulty": trek.difficulty,
        "duration": trek.duration,
        "total_slots": trek.total_slots,
        "available_slots": trek.available_slots,
        "assigned_staff": trek.assigned_staff,
        "start_date": str(trek.start_date) if trek.start_date else None,
        "end_date": str(trek.end_date) if trek.end_date else None,
        "status": trek.status,
        "is_deleted": trek.is_deleted,
        "description": trek.description
    }


def serialize_booking(booking):
    if not booking:
        return None
    return {
        "id": booking.id,
        "user_id": booking.user_id,
        "trek_id": booking.trek_id,
        "booking_date": str(booking.booking_date) if booking.booking_date else None,
        "number_of_people": booking.number_of_people,
        "status": booking.status,
        "user": {
            "name": booking.user.name,
            "email": booking.user.email
        } if booking.user else None,
        "trek": {
            "name": booking.trek.name,
            "location": booking.trek.location
        } if booking.trek else None
    }
