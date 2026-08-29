"""IFN636-11: auth/onboarding + Browse Fitness Classes (R1) + profile."""
from flask import render_template, request, redirect, url_for, session, flash

from db import get_db
from helpers import current_user, require_login


def seats_left(class_id):
    cls = get_db().timetable.find_one({"_id": class_id})
    if not cls:
        return 0
    return max(0, cls["seats"] - cls.get("seats_taken", 0))


def register_routes(app):
    # Lets templates check whether a route from a not-yet-built story exists
    # yet, so base.html/timetable.html degrade gracefully when run with only
    # a subset of the route modules registered (e.g. this batch on its own).
    app.jinja_env.globals["endpoint_exists"] = lambda name: name in app.view_functions

    @app.context_processor
    def inject_current_user():
        return {"current_user": current_user()}

    @app.route("/")
    def welcome():
        return render_template("welcome.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        success = request.args.get("success")
        if request.method == "POST":
            phone = request.form.get("phone", "").strip()
            password = request.form.get("password", "")
            user = get_db().users.find_one({"phone": phone})
            if user and (password == "" or password == user["password"]):
                session["user_phone"] = phone
                return redirect(url_for("home"))
            flash("We couldn't find an account with those details. Try again.", "error")
        return render_template(
            "login.html",
            success_banner="Signup Successful" if success else None,
        )

    @app.route("/register", methods=["GET", "POST"], endpoint="register")
    def register_view():
        if request.method == "POST":
            d = get_db()
            fullname = request.form.get("fullname", "").strip() or "New Member"
            email = request.form.get("email", "").strip()
            phone = request.form.get("phone", "").strip() or f"+61{d.users.count_documents({})+1000000}"
            password = request.form.get("password", "")
            d.users.replace_one(
                {"phone": phone},
                {
                    "name": fullname,
                    "email": email,
                    "phone": phone,
                    "location": "QLD, Australia",
                    "password": password,
                    "is_admin": False,
                },
                upsert=True,
            )
            return redirect(url_for("login", success=1))
        return render_template("register.html")

    @app.route("/logout")
    def logout():
        session.pop("user_phone", None)
        return redirect(url_for("welcome"))

    @app.route("/home")
    def home():
        if (r := require_login()):
            return r
        return render_template("home.html", show_nav=True, active="home")

    @app.route("/class/<slug>")
    def class_detail(slug):
        if (r := require_login()):
            return r
        d = get_db()
        cls = d.class_info.find_one({"_id": slug})
        if not cls:
            return redirect(url_for("home"))
        cls = {**cls, "slug": slug}
        others = [{"slug": c["_id"], "title": c["title"]} for c in d.class_info.find({"_id": {"$ne": slug}})]
        return render_template(
            "class_detail.html", cls=cls, other_classes=others, show_nav=True, active="home"
        )

    @app.route("/timetable")
    def timetable():
        if (r := require_login()):
            return r
        d = get_db()
        user = current_user()
        booked_ids = {
            b["class_id"]
            for b in d.bookings.find(
                {"status": "future", "user_phone": user["phone"]}, {"class_id": 1}
            )
        }
        days = ["S", "M", "T", "W", "T", "F", "S"]
        classes = [
            {**c, "id": c["_id"], "seats_left": seats_left(c["_id"])}
            for c in d.timetable.find().sort("_id")
        ]
        return render_template(
            "timetable.html",
            classes=classes,
            booked_ids=booked_ids,
            days=days,
            active_day=2,
            show_nav=True,
            active="timetable",
        )

    @app.route("/profile")
    def profile():
        if (r := require_login()):
            return r
        return render_template("profile.html", show_nav=True, active="profile")

    @app.route("/profile/edit", methods=["GET", "POST"])
    def profile_edit():
        if (r := require_login()):
            return r
        user = current_user()
        if request.method == "POST":
            updates = {
                "name": request.form.get("name", "").strip() or user["name"],
                "email": request.form.get("email", "").strip(),
                "location": request.form.get("location", "").strip(),
            }
            get_db().users.update_one({"phone": user["phone"]}, {"$set": updates})
            flash("Profile updated.")
            return redirect(url_for("profile"))
        return render_template("profile_edit.html", show_nav=True, active="profile")
