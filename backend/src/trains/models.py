from datetime import datetime
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship

from src.models import Base

class Train(Base):
    """
    Train Model.
    Tracks active rolling stock components moving dynamically across spatial linear routes.
    """
    __tablename__ = 'trains'

    train_id = Column(String(20), primary_key=True)
    current_station_id = Column(Integer, ForeignKey('stations.station_id', ondelete='SET NULL'), nullable=True)
    status = Column(String(30), nullable=False)
    current_speed = Column(Numeric(5, 2), default=0.00)
    headway_buffer_seconds = Column(Integer, default=180)
    last_ping_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    current_station = relationship("Station", back_populates="trains")

    # Index for fast lookup of trains by station
    __table_args__ = (
        Index('idx_trains_station', 'current_station_id'),
    )
