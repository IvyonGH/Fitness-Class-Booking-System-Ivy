"""IFN636-12: Book Fitness Classes (R2), capacity-safe."""
from flask import redirect, url_for, flash

from db import get_db, next_sequence
from helpers import current_user, require_login


def register_routes(app):
    @app.route("/timetable/book/<int:class_id>", methods=["POST"])
    def book_class(class_id):
        if (r := require_login()):
            return r
        user = current_user()
        if user and user.get("is_admin"):
            return redirect(url_for("timetable"))
        d = get_db()

        # A plain "seats_left > 0" check followed by a separate insert would let
        # two concurrent requests both pass the check and overbook the class.
        # find_one_and_update on a single document is atomic, so reserving a seat
        # (incrementing seats_taken, guarded by the same query) can't race.
        cls = d.timetable.find_one_and_update(
            {"_id": class_id, "$expr": {"$lt": ["$seats_taken", "$seats"]}},
            {"$inc": {"seats_taken": 1}},
        )
        if cls:
            d.bookings.insert_one({
                "id": next_sequence(d, "booking_id"),
                "class_id": class_id,
                "user_phone": user["phone"],
                "status": "future",
                "date": "28 Aug",
                "time": cls["time"],
                "name": cls["name"],
                "sub": cls["instructor"],
            })
            flash(f"Booked {cls['name']} at {cls['time']}.")
        return redirect(url_for("timetable"))
