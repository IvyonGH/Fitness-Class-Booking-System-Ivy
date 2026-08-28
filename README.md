# WonderFitness — Flask Prototype

A working clone of the Figma mockup, built with Flask (Python) + server-rendered
HTML/CSS. No JS framework, no build step — just `python app.py`.

## Run it

```bash
pip install -r requirements.txt
cp .env.example .env   # fill in MONGODB_URI with your Atlas connection string
python app.py
```

Users, classes, the timetable and bookings are stored in MongoDB (see
`db.py` / `seed.py`); the database is seeded automatically on first run.
Admin course/roster data is still in-memory pending its own migration.

Then open **http://127.0.0.1:5000** in your browser (resize to ~390px wide, or
open dev tools device mode, to see it as a phone screen — there's a phone
frame built into the CSS).

Log in with the seeded demo account: phone `+61412345678`, any password
(or leave password blank). Or just register a new account — it works.

## How the 21 Figma frames map to the app

Several frames in your Figma file are the *same screen* shown in different
fill states (empty vs. filled, before/after typing) rather than separate
destinations — e.g. Login_1/Login_2 are one Log In screen, and the three
Registration frames are one Register form filled in progressively. I built
one real, working page per screen rather than duplicating static states:

| Figma frame(s) | App route | Notes |
|---|---|---|
| Welcome | `/` | |
| Login_1, Login_2 | `/login` | same form; green "Login Successful" banner shows after registering |
| Registration_1/2/3 | `/register` | |
| Signup Successful | `/login?success=1` | redirect target after registering |
| Homepage | `/home` | category cards link into class detail |
| Timetable | `/timetable` | **Book** actually creates a booking |
| Pilates page | `/class/<slug>` | generic detail page, works for hiit/strength/pilates/trx |
| My Bookings | `/bookings?tab=future\|history\|cancelled` | **Cancel** actually cancels |
| Profile_1 | `/profile` | |
| Profile_2 | `/profile/edit` | **Save Change** actually updates the session user |
| Admin_Add ×2 | `/admin/create` | Create New Course form |
| Admin_Course ×2 | `/admin/course/<id>` | seeded with the two example courses from your mockup; **Edit** goes to `/admin/course/<id>/edit` (reuses the create form) |

## Structure

```
app.py                  Flask routes
db.py                    MongoDB connection helper (reads MONGODB_URI)
seed.py                  One-time demo data seeding
templates/               Jinja2 templates, one per screen
static/css/style.css     All styling — colors pulled from your mockup
```

## Known gaps / things to swap in

- **Images**: the HIIT/Strength/Pilates/TRX cards and class-detail hero use
  CSS gradient placeholders, not real photos (I don't have internet access
  to pull stock photography). Drop real images into `static/img/` and swap
  the `background-image` in `style.css` (`.cat-hiit`, `.cat-strength`, etc.
  and `.hero-img`).
- **Auth**: passwords are stored in plain text in memory — fine for a
  prototype, not for production.
- **Icons**: nav/social icons are emoji placeholders; swap for an icon font
  or SVGs if you want pixel-perfect icons.
