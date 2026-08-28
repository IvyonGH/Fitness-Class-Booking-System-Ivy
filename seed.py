"""Seeds MongoDB with the same demo data the old in-memory prototype shipped
with. Each collection is only seeded if it is currently empty, so this is
safe to call on every app startup.
"""

USERS = [
    {
        "phone": "+61412345678",
        "name": "Ted Mosby",
        "email": "t.mosby@out.edu.au",
        "location": "QLD, Australia",
        "password": "password",
        "is_admin": False,
    },
    {
        "phone": "+61400000000",
        "name": "Gym Admin",
        "email": "admin@wonderfitness.io",
        "location": "QLD, Australia",
        "password": "admin",
        "is_admin": True,
    },
]

CLASS_INFO = [
    {
        "_id": "hiit",
        "title": "HIIT",
        "description": "High Intensity Interval Training alternates short bursts of "
                        "all-out effort with brief recovery periods. It builds "
                        "cardiovascular fitness, torches calories, and improves "
                        "strength in a time-efficient 30-45 minute session.",
    },
    {
        "_id": "strength",
        "title": "Strength",
        "description": "Build lean muscle and functional power with progressive "
                        "resistance training. Sessions combine free weights, "
                        "machines and bodyweight work suited to all levels.",
    },
    {
        "_id": "pilates",
        "title": "Pilates",
        "description": "Pilates is a low impact workout that focuses on core "
                        "strength, flexibility and posture. Using controlled "
                        "movements and breathwork, it improves muscle tone, balance "
                        "and body awareness without putting stress on the joints. "
                        "Whether performed on a mat or reformer machine, Pilates is "
                        "suitable for all fitness levels and ages.",
    },
    {
        "_id": "trx",
        "title": "TRX",
        "description": "Suspension training using bodyweight and gravity to build "
                        "strength, balance, flexibility and core stability all at "
                        "once.",
    },
]

TIMETABLE = [
    {"_id": 1, "time": "6:00am", "duration": "60min", "name": "HIIT Beginner", "instructor": "Sam Wil", "seats": 15},
    {"_id": 2, "time": "7:00am", "duration": "60min", "name": "HIIT Beginner", "instructor": "Sam Wil", "seats": 15},
    {"_id": 3, "time": "7:00am", "duration": "50min", "name": "Strength+Leg", "instructor": "J.Jackson", "seats": 12},
    {"_id": 4, "time": "7:00am", "duration": "60min", "name": "Pilates Reformer", "instructor": "Jean Biber", "seats": 0},
    {"_id": 5, "time": "7:00am", "duration": "50min", "name": "Yoga", "instructor": "Wendy Vil", "seats": 10},
]


def seed_if_empty(db):
    if db.users.count_documents({}) == 0:
        db.users.insert_many(USERS)
    db.users.create_index("phone", unique=True)

    if db.class_info.count_documents({}) == 0:
        db.class_info.insert_many(CLASS_INFO)

    if db.timetable.count_documents({}) == 0:
        db.timetable.insert_many(TIMETABLE)
