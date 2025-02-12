"""
Todo:
    - Silence the "missing docstring" warning for the root files
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Geo(db.Model):
    """
    geo is short 'geographical point'

    @example: the geo point with the id=1 is Balbek Airbase in Crimea

    @naming: use 'Location' in future versions ?
    """
    __tablename__ = 'geo'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {"id": self.id, "name": self.name, "created_at": self.created_at}
