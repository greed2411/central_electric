from sqlalchemy import Column, DateTime, ForeignKey, Float, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    devices = relationship("Device", back_populates="owner")



class Device(Base):

    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    monthly_units = Column(Float)
    cost_per_unit = Column(Float)
    offline_duration = Column(Integer, default=0)
    accrued_interest = Column(Float, default=0.0)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="devices")
    events = relationship("LossEvent", back_populates="linked_device")



class LossEvent(Base):

    __tablename__ = "loss_events"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime)
    lapse = Column(Integer)
    loss_device_id = Column(Integer, ForeignKey("devices.id"))

    linked_device = relationship("Device", back_populates="events")
