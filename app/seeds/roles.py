from app.models import db, Role, environment, SCHEMA
roles = [
    Role(role_name='student', access_level=1),
    Role(role_name='instructor', access_level=2),
    Role(role_name='administrator', access_level=3),
    Role(role_name='superuser', access_level=99)
]


def seed_roles():
    for role in roles:
        db.session.add(role)

    db.session.commit()
    return


# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_roles():
    if environment == "production":
        db.session.execute(
            f"TRUNCATE table {SCHEMA}.roles RESTART IDENTITY CASCADE;")
    else:
        db.session.execute("DELETE FROM roles")

    db.session.commit()
