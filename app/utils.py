

from app.models import Device
from typing import Dict
from . import schemas

DAYS_IN_MONTH = 30
HOURS_IN_DAY = 24
MINUTES_IN_HOUR = 60
SECONDS_IN_MINUTE = 60
TIME_COMP_FACTOR = "1.{lapse}"

def calculate_lapse_interest(device: schemas.Device, lossevent: schemas.LossEventCreate):

    per_sec_unit = device.monthly_units / (DAYS_IN_MONTH * HOURS_IN_DAY * MINUTES_IN_HOUR * SECONDS_IN_MINUTE)
    calculated_interest = per_sec_unit * device.cost_per_unit * float(TIME_COMP_FACTOR.format(lapse=lossevent.lapse))
    return calculated_interest
    