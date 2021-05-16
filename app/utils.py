

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


def prepare_stream_payload(updated_device, lossevent_dict):

    updated_device_dict = updated_device.__dict__
    stream_payload = {}
    stream_payload["user_id"] = updated_device_dict["owner_id"]
    stream_payload["device_id"] = updated_device_dict["id"]
    stream_payload["accrued_interest"] = updated_device_dict["accrued_interest"]
    stream_payload["timestamp"] = lossevent_dict["timestamp"]
    return stream_payload