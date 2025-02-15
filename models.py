"""
Todo:
    - Move models to separate files
"""

import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB

db = SQLAlchemy()

class Geo(db.Model):
    """
    geo is short 'geographical point'

    @example: the geo point with the id=1 is Balbek Airbase in Crimea

    @naming: use 'Location' in future versions ?
    """
    __tablename__ = 'geo'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, server_default=db.func.now())

    # Note to myself: relationship does not store actual data in the table.
    # It dynamically loads related data when accessed.
    # It creates an abstraction for referencing foreign key
    # observations = db.relationship("Observation", back_populates="geos")

    def to_dict(self):
        return {"id": self.id, "name": self.name, "created_at": self.created_at}

class Observation(db.Model):
    """
    Analysis is a table that will store the results of the analysis for a given geographical point

    Attributes:
        id (int): Primary key, unique identifier for each observation.
        geo_id (int): Foreign key referencing the Geolocation table.
        date (date): The date when the observation was recorded.
        analysis (JSONB): A JSONB field containing observation data.
        asset_url (str): URL to the asset used for the observation.
        external_url (str): External URL to the source of the observation.

        created_at (timestamp): Timestamp indicating when the observation was created.
    """
    __tablename__ = 'observation'
    id = Column(Integer, primary_key=True)
    geo_id = Column(Integer, ForeignKey('geo.id', ondelete="SET NULL"), nullable=False)
    date = Column(DateTime, nullable=False)
    analysis = Column(JSONB, nullable=False)
    asset_url = Column(String(100), nullable=False)
    external_url = Column(String(100), nullable=False)

    created_at = Column(DateTime, server_default=db.func.now())

    # Relationship to Geo
    # geos = db.relationship("Geo", back_populates="observations")

    def to_dict(self):
        return {"id": self.id, "geo_id": self.geo_id, "analysis": json.dumps(self.analysis), "created_at": self.created_at}