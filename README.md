# WonderFitness — Flask Prototype

A working clone of the Figma mockup, built with Flask (Python) + server-rendered
HTML/CSS.

## Run it

```bash
pip install -r requirements.txt
cp .env.example .env
python app.py
```

Users, classes, the timetable and bookings are stored in MongoDB (see
`db.py` / `seed.py`); the database is seeded automatically on first run.
Admin course/roster data is still in-memory pending its own migration.

Then open **http://127.0.0.1:5000** in your browser, it is seen as a phone screen — there's a phone
frame built into the CSS).

Log in with the seeded demo account: 
user: phone `+61412345678`, any password(or leave password blank) Or just register a new account
admin: phone `+61400000000`, any password(or leave password blank)

| Figma frame(s) | App route | Notes |
|---|---|---|
| Welcome | `/` | |
| Login_1, Login_2 | `/login` | same form; green "Signup Successful" banner shows after registering |
| Registration_1/2/3 | `/register` | |
| Signup Successful | `/login?success=1` | redirect target after registering |
| Homepage | `/home` | category cards link into class detail |
| Schedule | `/timetable` | **Book** actually creates a booking |
| Pilates page | `/class/<slug>` | generic detail page, works for hiit/strength/pilates/trx |
| My Bookings | `/bookings?tab=future\|history\|cancelled` | **Cancel** actually cancels |
| Profile_1 | `/profile` | |
| Profile_2 | `/profile/edit` | **Save Change** actually updates the session user |
| Admin_Add ×2 | `/admin/create` | Create New Course form |
| Admin_Course ×2 | `/admin/course/<id>` | seeded with the two example courses from mockup; **Edit** goes to `/admin/course/<id>/edit` (reuses the create form) |

## Structure

```
app.py                   Flask routes
db.py                    MongoDB connection helper (reads MONGODB_URI)
seed.py                  One-time demo data seeding
templates/               Jinja2 templates, one per screen
static/css/style.css     All styling — colors pulled from your mockup
```
