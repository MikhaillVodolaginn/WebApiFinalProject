from typing import Type

from sqlalchemy.orm import Session

import schemas
from models import Country, City, Street


# Template
def get_model_list(db: Session, model: Type[Country | City | Street], skip: int = 0, limit: int = 10):
    return (db
            .query(model)
            .offset(skip)
            .limit(limit)
            .all())


def get_model(db: Session, model: Type[Country | City | Street], model_id: int):
    return (db
            .query(model)
            .filter_by(id=model_id)
            .first())


def update_model(
        db: Session,
        model: Type[Country | City | Street],
        model_id: int,
        model_data: schemas.CountryUpdate | schemas.CityUpdate | schemas.StreetUpdate | dict
):
    model_db = (db
                .query(model)
                .filter_by(id=model_id)
                .first())
    
    if not model_db:
        return None

    model_data = model_data if isinstance(model_data, dict) else model_data.model_dump()

    for key, value in model_data.items():
        if hasattr(model_db, key):
            setattr(model_db, key, value)

    db.commit()
    db.refresh(model_db)

    return model_db


def create_model(
        db: Session,
        model: Type[Country | City | Street],
        schema: schemas.CountryCreate | schemas.CityCreate | schemas.StreetCreate
):
    model_db = model(**schema.model_dump())

    db.add(model_db)
    db.commit()
    db.refresh(model_db)

    return model_db


def delete_model(db: Session, model: Type[Country | City | Street], model_id: int):
    model_db = (db
                .query(model)
                .filter_by(id=model_id)
                .first())

    if not model_db:
        return False

    db.delete(model_db)
    db.commit()

    return True


# Country
def get_country_list(db: Session, skip: int = 0, limit: int = 10):
    return get_model_list(db, Country, skip, limit)


def get_country(db: Session, country_id: int):
    return get_model(db, Country, country_id)


def update_country(db: Session, country_id: int, country_data: schemas.CountryUpdate | dict):
    return update_model(db, Country, country_id, country_data)


def create_country(db: Session, schema: schemas.CountryCreate):
    return create_model(db, Country, schema)


def delete_country(db: Session, country_id: int):
    return delete_model(db, Country, country_id)


# City
def get_city_list(db: Session, skip: int = 0, limit: int = 10):
    return get_model_list(db, City, skip, limit)


def get_city(db: Session, city_id: int):
    return get_model(db, City, city_id)


def update_city(db: Session, city_id: int, city_data: schemas.CityUpdate | dict):
    return update_model(db, City, city_id, city_data)


def create_city(db: Session, schema: schemas.CityCreate):
    return create_model(db, City, schema)


def delete_city(db: Session, city_id: int):
    return delete_model(db, City, city_id)


# Street
def get_street_list(db: Session, skip: int = 0, limit: int = 10):
    return get_model_list(db, Street, skip, limit)


def get_street(db: Session, street_id: int):
    return get_model(db, Street, street_id)


def update_street(db: Session, street_id: int, street_data: schemas.StreetUpdate | dict):
    return update_model(db, Street, street_id, street_data)


def create_street(db: Session, schema: schemas.StreetCreate):
    return create_model(db, Street, schema)


def delete_street(db: Session, street_id: int):
    delete_model(db, Street, street_id)
