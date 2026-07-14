from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from werkzeug.security import generate_password_hash
import redis

from application import workers
from application.config import Config
from application.models import db, User
from application.extensions import cache
from application.routes import auth, admin, staff, user

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)

db.init_app(app)
try:
    r = redis.Redis(host="localhost", port=6379, socket_timeout=1)
    r.ping()
    app.config["CACHE_TYPE"] = "RedisCache"
except Exception:
    app.config["CACHE_TYPE"] = "SimpleCache"
    print("Redis is offline. Falling back to SimpleCache.")

cache.init_app(app)
jwt = JWTManager(app)


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=int(identity)).one_or_none()

celery = workers.make_celery(app)
app.app_context().push()

import application.tasks

app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(staff)
app.register_blueprint(user)


@app.route("/")
def home():
    return {"message": "TrekTour REST API is running successfully."}, 200

with app.app_context():
    db.create_all()
    admin_user = User.query.filter_by(role="admin").first()
    if not admin_user:
        admin_user = User(
            username="admin",
            name="Administrator",
            email="admin@trek.com",
            phone="9999999999",
            password=generate_password_hash("admin123"),
            role="admin",
            status="approved"
        )

        db.session.add(admin_user)
        db.session.commit()
        print("Default Admin Created")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
