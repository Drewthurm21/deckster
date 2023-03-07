from app.models import db, Deck, environment, SCHEMA
from random import randint
from faker import Faker

fa = Faker()


def generate_deck(i):
    return Deck(
        owner_id=randint(1, 10),
        name=fa.text(max_nb_chars=30),
        description=fa.paragraph(nb_sentences=3),
        shared=i % 2 == 0
    )


def seed_decks():
    for deck in [generate_deck(i) for i in range(20)]:
        db.session.add(deck)

    db.session.commit()
    return


# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_decks():
    if environment == "production":
        db.session.execute(
            f"TRUNCATE table {SCHEMA}.decks RESTART IDENTITY CASCADE;")
    else:
        db.session.execute("DELETE FROM decks")

    db.session.commit()
