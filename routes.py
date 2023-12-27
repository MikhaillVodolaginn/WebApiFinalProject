from typing import List

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from crud import *
from database import get_db

ws_router = APIRouter()
country_router = APIRouter(prefix='/country', tags=['country'])
city_router = APIRouter(prefix='/city', tags=['city'])
street_router = APIRouter(prefix='/street', tags=['street'])


# WS
class ConnectManager:
    def __init__(self):
        self.connections: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.connections.append(ws)

    def disconnect(self, ws: WebSocket):
        self.connections.remove(ws)

    async def broadcast(self, message: str):
        for connection in self.connections:
            await connection.send_text(message)

    async def send_text_for_client(self, message: str, ws: WebSocket):
        await ws.send_text(message)


connectManager = ConnectManager()


async def notify_clients(message: str):
    for connection in connectManager.connections:
        await connection.send_text(message)


@ws_router.websocket("/ws/{client_id}")
async def websocket_endpoint(ws: WebSocket, client_id: int):
    await connectManager.connect(ws)
    await connectManager.broadcast(f"Congratulations! Client#{client_id} joined us")
    try:
        while True:
            receive_text = await ws.receive_text()
            await connectManager.send_text_for_client(f"You send message: {receive_text}", ws)
            await connectManager.broadcast(f"Client#{client_id} send message: {receive_text}")
    except WebSocketDisconnect:
        connectManager.disconnect(ws)
        await connectManager.broadcast(f"Unfortunately, Client#{client_id} left us")


# Country
@country_router.get("/", response_model=List[schemas.Country])
async def read_country_list(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    city_list = get_country_list(db, skip=skip, limit=limit)
    return city_list


@country_router.get("/{country_id}", response_model=schemas.Country)
async def read_country_by_id(country_id: int, db: Session = Depends(get_db)):
    city = get_country(db, country_id)
    return city


@country_router.patch("/{country_id}", response_model=schemas.Country)
async def update_country_by_id(country_id: int, country_data: schemas.CountryUpdate, db: Session = Depends(get_db)):
    country = update_country(db, country_id, country_data)

    if not country:
        await notify_clients(f"Failed to update country {country_id}")
        return {"message": f"country {country_id} not found"}

    await notify_clients(f"country {country.name} successfully updated")
    return country


@country_router.post("/", response_model=schemas.City)
async def create_country_by_id(country_data: schemas.CountryCreate, db: Session = Depends(get_db)):
    country = create_country(db, country_data)
    await notify_clients(f"country {country.name} successfully added to country list")
    return country


@country_router.delete("/{country_id}")
async def delete_country_by_id(country_id: int, db: Session = Depends(get_db)):
    country = delete_country(db, country_id)

    if not country:
        await notify_clients(f"Failed to delete country {country_id}")
        return {"message": f"country {country_id} not found"}

    await notify_clients(f"country {country_id} successfully deleted")
    return {"message": "country deleted"}


# City
@city_router.get("/", response_model=List[schemas.City])
async def read_city_list(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    city_list = get_city_list(db, skip=skip, limit=limit)
    return city_list


@city_router.get("/{city_id}", response_model=schemas.City)
async def read_city_by_id(city_id: int, db: Session = Depends(get_db)):
    city = get_city(db, city_id)
    return city


@city_router.patch("/{city_id}", response_model=schemas.City)
async def update_city_by_id(city_id: int, city_data: schemas.CityUpdate, db: Session = Depends(get_db)):
    city = update_city(db, city_id, city_data)

    if not city:
        await notify_clients(f"Failed to update city {city_id}")
        return {"message": f"city {city_id} not found"}

    await notify_clients(f"city {city.name} successfully updated")
    return city


@city_router.post("/", response_model=schemas.City)
async def create_city_by_id(city_data: schemas.CityCreate, db: Session = Depends(get_db)):
    city = create_city(db, city_data)
    await notify_clients(f"city {city.name} successfully added to city list")
    return city


@city_router.delete("/{city_id}")
async def delete_city_by_id(city_id: int, db: Session = Depends(get_db)):
    city = delete_city(db, city_id)

    if not city:
        await notify_clients(f"Failed to delete city {city_id}")
        return {"message": f"city {city_id} not found"}

    await notify_clients(f"city {city_id} successfully deleted")
    return {"message": "city deleted"}


# Street
@street_router.get("/", response_model=List[schemas.Street])
async def read_street_list(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_street_list(db, skip=skip, limit=limit)


@street_router.get("/{street_id}", response_model=schemas.Street)
async def read_street(street_id: int, db: Session = Depends(get_db)):
    return get_street(db, street_id)


@street_router.patch("/{street_id}")
async def update_street_by_id(street_id: int, schema: schemas.StreetUpdate, db: Session = Depends(get_db)):
    street = update_street(db, street_id, schema)

    if not street:
        await notify_clients(f"Failed to update city {street_id}")
        return {"message": f"street {street_id} not found"}

    await notify_clients(f"street {street_id} successfully updated")
    return {"message": "street updated"}


@street_router.post("/", response_model=schemas.Street)
async def create_street_by_id(schema: schemas.StreetCreate, db: Session = Depends(get_db)):
    street = create_street(db, schema)
    await notify_clients(f"street {street.name} successfully added")
    return street


@street_router.delete("/{street_id}")
async def delete_street_by_id(street_id: int, db: Session = Depends(get_db)):
    street = delete_street(db, street_id)

    if not street:
        await notify_clients(f"Failed to delete city {street_id}")
        return {"message": f"street {street_id} not found"}

    await notify_clients(f"street {street_id} successfully deleted")
    return {"message": "street deleted"}
