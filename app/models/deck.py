from .db import db, environment, SCHEMA
from sqlalchemy.orm import relationship


class Deck(db.Model):
    __tablename__ = 'decks'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(80))
    description = db.Column(db.String(255))
    shared = db.Column(db.Boolean, default=False)

    # Relationships
    owner = relationship('User', back_populates='decks')

    # Methods

    def to_dict(self):
        return {
            'id': self.id,
            'owner_id': self.owner_id,
            'name': self.name,
            'description': self.description,
            'shared': self.shared
        }
