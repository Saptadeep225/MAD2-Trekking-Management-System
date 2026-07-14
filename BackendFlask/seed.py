import sys
import os
import random
import string
from datetime import date, datetime, timedelta
from werkzeug.security import generate_password_hash
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app import app
from application.models import db, User, Trek, Booking

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_random_phone():
    return "9" + "".join(random.choices("0123456789", k=9))

def seed_data():
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Database tables reset.")
        admin = User(
            username="admin",
            name="Super Admin",
            email="admin@trek.com",
            phone="9999999999",
            password=generate_password_hash("admin123"),
            role="admin",
            status="approved"
        )
        db.session.add(admin)

        staff_members = []
        for i in range(1, 11):
            staff = User(
                username=f"staff{i}",
                name=f"Staff Member {i}",
                email=f"staff{i}@trek.com",
                phone=generate_random_phone(),
                password=generate_password_hash("staff123"),
                role="staff",
                status="approved"
            )
            db.session.add(staff)
            staff_members.append(staff)
        
        db.session.commit()
        print(f"Created {len(staff_members)} staff members.")

        users = []
        for i in range(1, 201):
            user = User(
                username=f"user{i}",
                name=f"Trekker {i}",
                email=f"user{i}@gmail.com",
                phone=generate_random_phone(),
                password=generate_password_hash("user123"),
                role="user",
                status="approved"
            )
            db.session.add(user)
            users.append(user)
        
        db.session.commit()
        print(f"Created {len(users)} users.")

        locations = ["Himachal Pradesh", "Uttarakhand", "Sikkim", "Kashmir", "West Bengal", "Maharashtra", "Karnataka", "Kerala"]
        adjectives = ["Majestic", "Hidden", "Beautiful", "Serene", "Wild", "Misty", "Snowy", "Lush"]
        nouns = ["Peak", "Valley", "Pass", "Lake", "Meadow", "Trail", "Ridge", "Glacier"]
        
        treks = []
        for i in range(1, 51):
            start = date.today() + timedelta(days=random.randint(-10, 60))
            duration = random.randint(2, 12)
            end = start + timedelta(days=duration)
            total = random.randint(10, 50)
            
            trek = Trek(
                name=f"{random.choice(adjectives)} {random.choice(nouns)} Trek",
                location=random.choice(locations),
                difficulty=random.choice(["Easy", "Moderate", "Hard"]),
                duration=duration,
                total_slots=total,
                available_slots=total,
                assigned_staff=random.choice(staff_members).id,
                start_date=start,
                end_date=end,
                status=random.choice(["Open", "Completed", "Pending"]),
                description=f"A wonderful {duration} days trek in the heart of the mountains. Perfect for adventure enthusiasts."
            )
            db.session.add(trek)
            treks.append(trek)
            
        db.session.commit()
        print(f"Created {len(treks)} treks.")

        bookings_count = 0
        for user in users:
            num_bookings = random.randint(0, 5)
            booked_treks = random.sample(treks, min(num_bookings, len(treks)))
            for trek in booked_treks:
                if trek.available_slots > 0:
                    pax = random.randint(1, min(4, trek.available_slots))
                    booking = Booking(
                        user_id=user.id,
                        trek_id=trek.id,
                        booking_date=datetime.now() - timedelta(days=random.randint(1, 30)),
                        number_of_people=pax,
                        status=random.choice(["Booked", "Completed", "Cancelled"])
                    )
                    trek.available_slots -= pax
                    db.session.add(booking)
                    bookings_count += 1
        
        db.session.commit()
        print(f"Created {bookings_count} bookings.")
        print("Randomised dataset generation complete!")

if __name__ == '__main__':
    seed_data()
