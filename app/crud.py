from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    # TODO: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/?h=hash#password-hashing
    # hash the pwd using passlib
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(username=user.username, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_device(db: Session, device_id: int):
    return db.query(models.Device).filter(models.Device.id == device_id).first()


def get_devices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Device).offset(skip).limit(limit).all()


def update_device(db: Session, device_id: int, lapse_interest: float):
    device = db.query(models.Device).filter(models.Device.id == device_id).first()
    device.accrued_interest += lapse_interest
    device.offline_duration += 1
    db.add(device)
    db.commit()
    db.refresh(device)
    return device


def create_user_device(db: Session, device: schemas.DeviceCreate, user_id: int):
    db_device = models.Device(**device.dict(), owner_id=user_id)
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device


def create_device_lossevent(db: Session, lossevent: schemas.LossEvent, device_id: int):
    db_lossevent = models.LossEvent(**lossevent.dict(), loss_device_id=device_id)
    db.add(db_lossevent)
    db.commit()
    db.refresh(db_lossevent)
    return db_lossevent