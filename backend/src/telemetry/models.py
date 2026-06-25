from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship

from src.models import Base

class TelemetryLog(Base):
    """
    TelemetryLog Model.
    Maintains transactional time-series metadata used for post-incident audits and downstream ML prediction modules.
    """
    __tablename__ = 'telemetry_logs'

    log_id = Column(Integer, primary_key=True, autoincrement=True)
    station_id = Column(Integer, ForeignKey('stations.station_id', ondelete='CASCADE'), nullable=True)
    tap_in_count = Column(Integer, nullable=False)
    tap_out_count = Column(Integer, nullable=False)
    estimated_platform_count = Column(Integer, nullable=False)
    recorded_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    station = relationship("Station", back_populates="telemetry_logs")

    # Index for efficient chronological log scanning per station
    __table_args__ = (
        Index('idx_telemetry_station_time', 'station_id', 'recorded_at'),
    )
