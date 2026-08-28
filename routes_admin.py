"""IFN636-14: View Attendance Roster (R4) / admin course management."""
from flask import render_template, request, redirect, url_for, flash

from db import get_db, next_sequence
from helpers import current_user, require_login


def require_admin():
    user = current_user()
    if not user or not user.get("is_admin"):
        return redirect(url_for("home"))
    return None


def find_course(course_id):
    course = get_db().courses.find_one({"_id": course_id})
    if not course:
        return None
    return {**course, "id": course["_id"]}


def register_routes(app):
    @app.route("/admin/courses")
    def admin_courses_list():
        if (r := require_login()):
            return r
        if (r := require_admin()):
            return r
        d = get_db()
        courses = [{**c, "id": c["_id"]} for c in d.courses.find().sort("_id")]
        return render_template(
            "admin_courses_list.html", courses=courses, show_nav=True, active="admin_list"
        )

    @app.route("/admin/create", methods=["GET", "POST"])
    def admin_create():
        if (r := require_login()):
            return r
        if (r := require_admin()):
            return r
        if request.method == "POST":
            d = get_db()
            course_id = next_sequence(d, "course_id")
            d.courses.insert_one({
                "_id": course_id,
                "datetime": request.form.get("datetime", "").strip(),
                "course_type": request.form.get("course_type", "").strip(),
                "instructor": request.form.get("instructor", "").strip(),
                "seats": request.form.get("seats", "").strip(),
                "description": request.form.get("description", "").strip(),
                "attendees": [],
            })
            flash("Course created.")
            return redirect(url_for("admin_courses_list"))
        return render_template("admin_create.html", course=None, show_nav=True, active="admin")

    @app.route("/admin/course/<int:course_id>")
    def admin_course_detail(course_id):
        if (r := require_login()):
            return r
        if (r := require_admin()):
            return r
        course = find_course(course_id)
        if not course:
            return redirect(url_for("admin_courses_list"))
        return render_template(
            "admin_course_detail.html", course=course, show_nav=True, active="admin_list"
        )

    @app.route("/admin/course/<int:course_id>/edit", methods=["GET", "POST"])
    def admin_edit_course(course_id):
        if (r := require_login()):
            return r
        if (r := require_admin()):
            return r
        course = find_course(course_id)
        if not course:
            return redirect(url_for("admin_courses_list"))
        if request.method == "POST":
            updates = {
                "datetime": request.form.get("datetime", "").strip(),
                "course_type": request.form.get("course_type", "").strip(),
                "instructor": request.form.get("instructor", "").strip(),
                "seats": request.form.get("seats", "").strip(),
                "description": request.form.get("description", "").strip(),
            }
            get_db().courses.update_one({"_id": course_id}, {"$set": updates})
            flash("Course updated.")
            return redirect(url_for("admin_course_detail", course_id=course_id))
        return render_template("admin_create.html", course=course, show_nav=True, active="admin")

    @app.route("/admin/course/<int:course_id>/attendee/<int:index>/cancel", methods=["POST"])
    def cancel_attendee(course_id, index):
        if (r := require_login()):
            return r
        if (r := require_admin()):
            return r
        course = find_course(course_id)
        if course and 0 <= index < len(course["attendees"]):
            removed = course["attendees"].pop(index)
            get_db().courses.update_one(
                {"_id": course_id}, {"$set": {"attendees": course["attendees"]}}
            )
            flash(f"Removed {removed['name']}.")
        return redirect(url_for("admin_course_detail", course_id=course_id))
