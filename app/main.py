from typing import Dict, List

from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, WebSocket, WebSocketDisconnect

from . import crud, models, schemas, utils, producer
from .database import SessionLocal, engine


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

websocket_connection_manager : Dict[int, WebSocket]= {}

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="username already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/devices/", response_model=schemas.Device)
def create_device_for_user(
    user_id: int, device: schemas.DeviceCreate, db: Session = Depends(get_db)
):
    return crud.create_user_device(db=db, device=device, user_id=user_id)


@app.get("/devices/", response_model=List[schemas.Device])
def read_devices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    devices = crud.get_devices(db, skip=skip, limit=limit)
    return devices


@app.websocket("/device/ws/{device_id}")
async def websocket_endpoint(websocket: WebSocket, device_id: int, db: Session = Depends(get_db)):

    await websocket.accept()

    try:
        
        while True:
            lossevent_dict = await websocket.receive_json()
            lossevent = schemas.LossEventCreate(**lossevent_dict)
            device = crud.get_device(db=db, device_id=device_id)
            lapse_interest = utils.calculate_lapse_interest(device, lossevent)
            _ = crud.create_device_lossevent(db=db, lossevent=lossevent, device_id=device_id)
            updated_device = crud.update_device(db=db, device_id=device_id, lapse_interest=lapse_interest)
            stream_payload = utils.prepare_stream_payload(updated_device, lossevent_dict)
            producer.send_lossevent_into_rmq(stream_payload)
            await websocket.send_json({**lossevent_dict})

    except WebSocketDisconnect:
        print(f"device: {device_id} dropped connection!")


@app.websocket("/listener/ws")
@app.websocket("/user/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int = None):

    await websocket.accept()

    if user_id:
        websocket_connection_manager[user_id] = websocket

    try:
        
        while True:
            # websocket incoming only from worker
            published_lossevent_dict = await websocket.receive_json()   
            to_update_user_id = published_lossevent_dict["user_id"]

            if to_update_user_id in websocket_connection_manager.keys():
                to_update_user_websocket = websocket_connection_manager[to_update_user_id]
                # websocket outgoing only to end-user
                await to_update_user_websocket.send_json(published_lossevent_dict)

    except WebSocketDisconnect:
        if user_id:
            print(f"user: {user_id} dropped connection!")
            websocket_connection_manager.pop(user_id, None)
