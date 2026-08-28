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
    {"_id": 1, "time": "6:00am", "duration": "60min", "name": "HIIT Beginner", "instructor": "Sam Wil", "seats": 15, "seats_taken": 0},
    {"_id": 2, "time": "7:00am", "duration": "60min", "name": "HIIT Beginner", "instructor": "Sam Wil", "seats": 15, "seats_taken": 0},
    {"_id": 3, "time": "7:00am", "duration": "50min", "name": "Strength+Leg", "instructor": "J.Jackson", "seats": 12, "seats_taken": 0},
    {"_id": 4, "time": "7:00am", "duration": "60min", "name": "Pilates Reformer", "instructor": "Jean Biber", "seats": 0, "seats_taken": 0},
    {"_id": 5, "time": "7:00am", "duration": "50min", "name": "Yoga", "instructor": "Wendy Vil", "seats": 10, "seats_taken": 0},
]

COURSES = [
    {
        "_id": 1,
        "datetime": "26 Aug 6:00 am",
        "course_type": "HIIT Beginner",
        "instructor": "Sam Will",
        "seats": "15",
        "description": "A beginner-friendly HIIT class designed to build stamina, "
                        "boost energy, and improve overall fitness through simple, "
                        "low-impact intervals. Perfect for newcomers who want an "
                        "effective workout without complex movements.",
        "attendees": [
            {"name": "Avery Lane", "gender": "F", "age": 42, "membership": "8m"},
            {"name": "Jordan Crest", "gender": "M", "age": 32, "membership": "3y2m"},
            {"name": "Casey Rowan", "gender": "F", "age": 22, "membership": "6m"},
            {"name": "Jamie Calder", "gender": "F", "age": 23, "membership": "6m"},
            {"name": "Skylar Hale", "gender": "M", "age": 35, "membership": "2y"},
            {"name": "Hana Rivers", "gender": "F", "age": 52, "membership": "6y"},
            {"name": "Lex Marlow", "gender": "M", "age": 30, "membership": "3y"},
        ],
    },
    {
        "_id": 2,
        "datetime": "02 Sep 8:00 am",
        "course_type": "Pilates Reformer",
        "instructor": "Jean Biber",
        "seats": "12",
        "description": "Step into a Reformer course built for power, precision, "
                        "and flow. Using the Reformer's sliding carriage and "
                        "adjustable springs, you'll challenge your core, sculpt "
                        "your muscles, and unlock mobility you didn't know you "
                        "had. Each class is fast-moving, technique-driven, and "
                        "designed to leave you feeling strong, aligned, and "
                        "unstoppable.",
        "attendees": [
            {"name": "Riley Osborn", "gender": "F", "age": 29, "membership": "1y4m"},
            {"name": "Morgan Blake", "gender": "M", "age": 41, "membership": "5y"},
            {"name": "Quinn Sinclair", "gender": "F", "age": 26, "membership": "3m"},
        ],
    },
]


def seed_if_empty(db):
    if db.users.count_documents({}) == 0:
        db.users.insert_many(USERS)
    db.users.create_index("phone", unique=True)

    if db.class_info.count_documents({}) == 0:
        db.class_info.insert_many(CLASS_INFO)

    if db.timetable.count_documents({}) == 0:
        db.timetable.insert_many(TIMETABLE)

    if db.courses.count_documents({}) == 0:
        db.courses.insert_many(COURSES)
        db.counters.update_one(
            {"_id": "course_id"}, {"$set": {"seq": len(COURSES)}}, upsert=True
        )
