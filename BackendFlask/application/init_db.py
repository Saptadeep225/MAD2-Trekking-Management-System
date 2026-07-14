import sys
import os
import random
from datetime import date, datetime, timedelta
from werkzeug.security import generate_password_hash

# Add parent directory to path to allow import of app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from application.models import db, User, Trek, Booking


def init_db():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        print("Database tables created.")

        # Create Default Admin
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
        print("Default Admin Created.")

        staff_names = ["Rahul", "Amit", "Priya", "Sneha", "Rohit"]
        staff_members = []
        for i, name in enumerate(staff_names, start=1):
            staff = User(
                username=f"staff{i}",
                name=name,
                email=f"staff{i}@trek.com",
                phone=f"98765432{i:02}",
                password=generate_password_hash("staff123"),
                role="staff",
                status="approved"
            )
            db.session.add(staff)
            staff_members.append(staff)
        db.session.commit()
        print("Staff members created.")

        # Users
        first_names = [
            "Arjun", "Neha", "Karan", "Riya", "Ankit",
            "Soham", "Ananya", "Aisha", "Vikram", "Meera",
            "Rohan", "Diya", "Aman", "Pooja", "Ishaan",
            "Kabir", "Nisha", "Dev", "Tina", "Yash"
        ]
        users = []
        for i, name in enumerate(first_names, start=1):
            user = User(
                username=f"user{i}",
                name=name,
                email=f"user{i}@gmail.com",
                phone=f"900000{i:04}",
                password=generate_password_hash("user123"),
                role="user",
                status="approved"
            )
            db.session.add(user)
            users.append(user)
        db.session.commit()
        print("Trekkers (users) created.")

        # Treks
        trek_data = [
            ("Sandakphu", "West Bengal", "Hard"),
            ("Kedarkantha", "Uttarakhand", "Easy"),
            ("Hampta Pass", "Himachal Pradesh", "Moderate"),
            ("Triund", "Himachal Pradesh", "Easy"),
            ("Valley of Flowers", "Uttarakhand", "Moderate"),
            ("Tarsar Marsar", "Kashmir", "Hard"),
            ("Goechala", "Sikkim", "Hard"),
            ("Brahmatal", "Uttarakhand", "Moderate"),
            ("Nag Tibba", "Uttarakhand", "Easy"),
            ("Dzongri", "Sikkim", "Moderate")
        ]
        treks = []
        for i, trek in enumerate(trek_data):
            total = random.randint(20, 40)
            start = date.today() + timedelta(days=random.randint(5, 90))
            end = start + timedelta(days=random.randint(2, 8))
            obj = Trek(
                name=trek[0],
                location=trek[1],
                difficulty=trek[2],
                duration=(end - start).days,
                total_slots=total,
                available_slots=total,
                assigned_staff=random.choice(staff_members).id,
                start_date=start,
                end_date=end,
                status="Open",
                description=f"Experience the beauty of {trek[0]}."
            )
            db.session.add(obj)
            treks.append(obj)
        db.session.commit()
        print("Treks created.")

        # Bookings
        for user in users:
            booked = random.sample(treks, random.randint(1, 3))
            for trek in booked:
                if trek.available_slots <= 0:
                    continue
                booking = Booking(
                    user_id=user.id,
                    trek_id=trek.id,
                    booking_date=datetime.now() - timedelta(days=random.randint(1, 30)),
                    number_of_people=1,
                    status=random.choice(["Booked", "Completed"])
                )
                trek.available_slots -= 1
                db.session.add(booking)
        db.session.commit()
        print("Bookings created.")
        print("Database Seeded Successfully!")


if __name__ == "__main__":
    init_db()
