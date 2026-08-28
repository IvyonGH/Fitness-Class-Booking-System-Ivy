"""
WonderFitness -- functional prototype built from Figma design.

Run:
    pip install -r requirements.txt
    python app.py
Then open http://127.0.0.1:5000
"""
import os

from flask import Flask

from db import get_db
from seed import seed_if_empty
import routes_browse
import routes_booking

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-placeholder-not-for-production")

routes_browse.register_routes(app)
routes_booking.register_routes(app)

if __name__ == "__main__":
    seed_if_empty(get_db())
    app.run(debug=True)
