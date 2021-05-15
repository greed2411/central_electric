from app.models import LossEvent
from typing import List
from datetime import datetime
from pydantic import BaseModel


class DeviceBase(BaseModel):

    monthly_units : float
    cost_per_unit: float


class DeviceCreate(DeviceBase):
    pass


class UserBase(BaseModel):

    username: str


class UserCreate(UserBase):

    password: str


class LossEventBase(BaseModel):

    timestamp: datetime
    lapse: int


class LossEventCreate(LossEventBase):
    pass
    

class LossEvent(LossEventBase):
    id: int
    loss_device_id: int

    class Config:
        orm_mode = True


class Device(DeviceBase):
    id: int
    owner_id: int
    accrued_interest: float
    events: List[LossEvent] = []

    class Config:
        orm_mode = True


class User(UserBase):
    id: int
    devices: List[Device] = []

    class Config:
        orm_mode = True