from app.models import db, User, environment, SCHEMA
from werkzeug.security import generate_password_hash
from faker import Faker

# Adds a demo user, you can add other users here if you want
fa = Faker()
demo = User(username='Demo', email='demo@aa.io',
            password='password', role_id=1)


def generate_user():
    return User(
        username=fa.name(),
        email=fa.ascii_free_email(),
        role_id=1,
        hashed_password=generate_password_hash(fa.password())
    )


def seed_users():
    db.session.add(demo)
    for user in [generate_user() for _ in range(9)]:
        db.session.add(user)

    db.session.commit()
    return


# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_users():
    if environment == "production":
        db.session.execute(
            f"TRUNCATE table {SCHEMA}.users RESTART IDENTITY CASCADE;")
    else:
        db.session.execute("DELETE FROM users")

    db.session.commit()
