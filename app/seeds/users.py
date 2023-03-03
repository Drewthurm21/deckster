from app.models import db, User, environment, SCHEMA
from werkzeug.security import generate_password_hash
from faker import Faker

# Adds a demo user, you can add other users here if you want
fa = Faker()


def generate_user():
    return User(
        username=fa.name(),
        email=fa.ascii_free_email(),
        role_id=1,
        hashed_password=generate_password_hash(fa.password())
    )


def seed_users():
    demo = User(username='Demo', email='demo@aa.io',
                password='password', role_id=1)
    db.session.add(demo)
    users = [generate_user() for _ in range(9)]
    for user in users:
        print(f'Adding user: {user.to_dict()} \n')
        db.session.add(user)

    print('Commit to db:')
    db.session.commit()

    print('Seed Users complete')
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
