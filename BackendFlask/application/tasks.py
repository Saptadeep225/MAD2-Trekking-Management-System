from celery import Celery
from celery.schedules import crontab
from datetime import datetime, date, timedelta
import os
import csv
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from application.models import db, User, Trek, Booking
from application.workers import make_celery
from app import app


celery_app = make_celery(app)


def send_email(recipient, subject, body):
    msg = MIMEMultipart()
    msg["From"] = app.config.get("SENDER_EMAIL", "admin@trek.com")
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))
    
    mail_server = app.config.get("MAIL_SERVER", "localhost")
    mail_port = app.config.get("MAIL_PORT", 1025)
    sender_email = app.config.get("SENDER_EMAIL")
    sender_password = app.config.get("SENDER_PASSWORD")
    
    try:
        with smtplib.SMTP(host=mail_server, port=mail_port) as server:
            if sender_email and sender_password:
                server.login(sender_email, sender_password)
            server.send_message(msg)
            print(f"Sent email to {recipient}")
    except Exception as e:
        print(f"Failed to send email to {recipient}: {str(e)}")


def add_user_notification(user_id, message, download_url=None):
    folder = os.path.join(app.root_path, "instance", "notifications")
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, f"{user_id}.json")
    
    notifications = []
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                notifications = json.load(f)
        except Exception:
            notifications = []
            
    notifications.append({
        "message": message,
        "download_url": download_url,
        "timestamp": datetime.now().isoformat()
    })
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(notifications, f, indent=4)


@celery_app.task
def export_bookings_csv(user_id, username):
    export_dir = os.path.join(app.root_path, "static", "exports")
    os.makedirs(export_dir, exist_ok=True)
    
    filename = f"booking_history_{username}.csv"
    filepath = os.path.join(export_dir, filename)
    
    bookings = Booking.query.filter_by(user_id=user_id).all()
    
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["User ID", "Trek Name", "Location", "Booking Status", "Start Date", "End Date", "Booking Date"])
        for b in bookings:
            writer.writerow([
                b.user_id,
                b.trek.name if b.trek else "Unknown Trek",
                b.trek.location if b.trek else "Unknown Location",
                b.status,
                str(b.trek.start_date) if (b.trek and b.trek.start_date) else "",
                str(b.trek.end_date) if (b.trek and b.trek.end_date) else "",
                str(b.booking_date) if b.booking_date else ""
            ])
            
    download_url = f"/static/exports/{filename}"
    add_user_notification(user_id, "Booking history exported successfully. Click here to download.", download_url)
    print(f"Exported booking history for user {username} to {filepath}")


@celery_app.task
def send_daily_reminders():
    tomorrow = date.today() + timedelta(days=1)
    upcoming_treks = Trek.query.filter_by(start_date=tomorrow, is_deleted=False).all()
    
    count = 0
    for trek in upcoming_treks:
        for booking in trek.bookings:
            if booking.status == "Booked":
                subject = f"Upcoming Trek Reminder: {trek.name}"
                recipient = booking.user.email
                body = f"""
                <html>
                <body>
                    <h2>Hello {booking.user.name},</h2>
                    <p>This is a reminder that your booking for the trek <strong>{trek.name}</strong> is starting tomorrow ({trek.start_date}).</p>
                    <p><strong>Trek Details:</strong></p>
                    <ul>
                        <li>Location: {trek.location}</li>
                        <li>Duration: {trek.duration} days</li>
                        <li>Difficulty: {trek.difficulty}</li>
                    </ul>
                    <p>Please make sure you have all necessary gear and arrive on time. Safe travels!</p>
                </body>
                </html>
                """
                send_email(recipient, subject, body)
                count += 1
                
    return f"Sent {count} daily reminders."


@celery_app.task
def send_monthly_report():
    first_day_this_month = date.today().replace(day=1)
    last_day_prev_month = first_day_this_month - timedelta(days=1)
    first_day_prev_month = last_day_prev_month.replace(day=1)
    
    total_treks_conducted = Trek.query.filter(Trek.start_date >= first_day_prev_month, Trek.start_date <= last_day_prev_month).count()
    total_bookings = Booking.query.filter(Booking.booking_date >= datetime.combine(first_day_prev_month, datetime.min.time()), Booking.booking_date <= datetime.combine(last_day_prev_month, datetime.max.time())).count()
    
    popular = db.session.query(
        Trek.name, db.func.count(Booking.id).label("booking_count")
    ).join(Booking, Trek.id == Booking.trek_id)\
     .filter(Booking.booking_date >= first_day_prev_month, Booking.booking_date <= last_day_prev_month)\
     .group_by(Trek.id).order_by(db.func.count(Booking.id).desc()).limit(5).all()
     
    popular_html = "".join([f"<li>{name}: {count} bookings</li>" for name, count in popular])
    
    subject = f"Monthly Trekking Activity Report - {first_day_prev_month.strftime('%B %Y')}"
    recipient = "admin@trek.com"
    body = f"""
    <html>
    <body>
        <h2>Monthly Trekking Activity Report ({first_day_prev_month.strftime('%B %Y')})</h2>
        <p>Hello Admin,</p>
        <p>Here are the statistics for the past month:</p>
        <ul>
            <li><strong>Treks Conducted:</strong> {total_treks_conducted}</li>
            <li><strong>Total Participants / Bookings:</strong> {total_bookings}</li>
        </ul>
        <h3>Popular Treks:</h3>
        <ol>
            {popular_html or "<li>No treks booked in this period.</li>"}
        </ol>
    </body>
    </html>
    """
    send_email(recipient, subject, body)
    return "Monthly report sent to Admin."


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=8, minute=0), send_daily_reminders.s(), name="Daily Reminder")
    sender.add_periodic_task(crontab(day_of_month=1, hour=0, minute=0), send_monthly_report.s(), name="Monthly Report")
celery_app.conf.timezone = 'IST'
