"""Auth helpers shared by every route module."""
from flask import session, redirect, url_for

from db import get_db


def current_user():
    phone = session.get("user_phone")
    if not phone:
        return None
    return get_db().users.find_one({"phone": phone})


def require_login():
    if not session.get("user_phone"):
        return redirect(url_for("login"))
    return None
