from .db import db, environment, SCHEMA
from sqlalchemy.orm import relationship


class Role(db.Model):
    __tablename__ = 'roles'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(40), nullable=False)
    access_level = db.Column(db.Integer, nullable=False)

    # Relationships
    users = relationship('User', back_populates='user_role')

    def to_dict(self):
        return {
            'id': self.id,
            'role_name': self.role_name,
            'access_level': self.access_level
        }
