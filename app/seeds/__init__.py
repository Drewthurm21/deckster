from flask.cli import AppGroup
from .users import seed_users, undo_users
from .roles import seed_roles, undo_roles
from .decks import seed_decks, undo_decks
from app.models.db import db, environment, SCHEMA

# Creates a seed group to hold our commands
seed_commands = AppGroup('seed')


# Creates the `flask seed all` command
@seed_commands.command('all')
def seed():
    if environment == 'production':
        # Before seeding in production, you want to run the seed undo
        # command, which will truncate all tables prefixed with
        # the schema name (see comment in users.py undo_users function).
        # Make sure to add all your other model's undo functions below
        undo_decks()
        undo_users()
        undo_roles()
    seed_roles()
    seed_users()
    seed_decks()
    # Add other seed functions here


# Creates the `flask seed undo` command
@seed_commands.command('undo')
def undo():
    undo_decks()
    undo_users()
    undo_roles()
    # Add other undo functions here
