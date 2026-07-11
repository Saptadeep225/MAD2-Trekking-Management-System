from flask import Blueprint, request
from flask_restful import Api, Resource
from flask_jwt_extended import create_access_token, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from application.models import db, User

auth = Blueprint("auth", __name__, url_prefix="/auth")
auth_api = Api(auth)


class LoginResource(Resource):
    def post(self):
        data = request.get_json(silent=True) or {}
        username = data.get("username", "").strip()
        password = data.get("password", "")

        if not username or not password:
            return {"message": "Invalid username or password."}, 400

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            if user.role == "staff" and user.status == "pending":
                return {"message": "Your account is waiting for admin approval."}, 403
            if user.status == "blacklisted":
                return {"message": "Your account has been blacklisted by the administrator."}, 403

            access_token = create_access_token(identity=str(user.id))
            return {
                "message": f"Welcome back, {user.name}!",
                "access_token": access_token,
                "role": user.role,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "name": user.name,
                    "email": user.email,
                    "phone": user.phone,
                    "status": user.status
                }
            }, 200

        return {"message": "Invalid username or password."}, 401


class RegisterResource(Resource):
    def post(self):
        data = request.get_json(silent=True) or {}
        username = data.get("username", "").strip()
        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        phone = data.get("phone", "").strip()
        password = data.get("password", "")
        confirm_password = data.get("confirm_password", "")
        role = data.get("role", "user")
        if role not in ["user", "staff"]:
            role = "user"

        # Validation
        if not username or not name or not email or not password:
            return {"message": "Please fill all required fields."}, 400
        if password != confirm_password:
            return {"message": "Passwords do not match."}, 400
        if len(password) < 6:
            return {"message": "Password must be at least 6 characters."}, 400
        if User.query.filter_by(username=username).first():
            return {"message": "Username already exists."}, 400
        if User.query.filter_by(email=email).first():
            return {"message": "Email already registered."}, 400

        status = "pending" if role == "staff" else "approved"
        new_user = User(
            username=username,
            name=name,
            email=email,
            phone=phone,
            password=generate_password_hash(password),
            role=role,
            status=status
        )
        db.session.add(new_user)
        db.session.commit()
        return {"message": "Registration successful! Please login."}, 201


class LogoutResource(Resource):
    @jwt_required()
    def post(self):
        return {"message": "Logged out successfully."}, 200


auth_api.add_resource(LoginResource, "/login")
auth_api.add_resource(RegisterResource, "/register")
auth_api.add_resource(LogoutResource, "/logout")
