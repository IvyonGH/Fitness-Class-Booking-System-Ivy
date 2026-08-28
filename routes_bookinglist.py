"""IFN636-13: View Booking List (R3), owner-scoped."""
from flask import render_template, request, redirect, url_for, flash

from db import get_db
from helpers import current_user, require_login


def register_routes(app):
    @app.route("/bookings")
    def bookings():
        if (r := require_login()):
            return r
        tab = request.args.get("tab", "future")
        user = current_user()
        d = get_db()
        # Records are limited to the member who made them (plus admins, who use
        # the separate roster view for other members' bookings).
        query = {"status": tab} if user.get("is_admin") else {"status": tab, "user_phone": user["phone"]}
        items = list(d.bookings.find(query).sort("id", -1))
        return render_template(
            "bookings.html", items=items, tab=tab, show_nav=True, active="bookings"
        )

    @app.route("/bookings/cancel/<int:booking_id>", methods=["POST"])
    def cancel_booking(booking_id):
        if (r := require_login()):
            return r
        user = current_user()
        d = get_db()
        query = {"id": booking_id, "status": "future"}
        if not user.get("is_admin"):
            query["user_phone"] = user["phone"]
        booking = d.bookings.find_one_and_update(query, {"$set": {"status": "cancelled"}})
        if booking:
            d.timetable.update_one({"_id": booking["class_id"]}, {"$inc": {"seats_taken": -1}})
            flash("Booking cancelled.")
        return redirect(url_for("bookings", tab="future"))
