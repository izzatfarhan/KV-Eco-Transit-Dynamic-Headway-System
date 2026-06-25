from datetime import datetime
from sqlalchemy import Column, Integer, String, Numeric, DateTime
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from backend.src.models import Base

class Station(Base):
    """
    Station Model.
    Maintains geometric boundaries, identifiers, and real-time aggregate commuter load metrics across the urban rail network.
    """
    __tablename__ = 'stations'

    station_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    line_name = Column(String(50), nullable=False)
    geo_location = Column(Geometry(geometry_type='POINT', srid=4326), nullable=True)
    current_crowd_density = Column(Numeric(3, 2), default=0.00)
    passenger_arrival_rate_per_min = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    trains = relationship("Train", back_populates="current_station")
    telemetry_logs = relationship("TelemetryLog", back_populates="station", cascade="all, delete-orphan")
