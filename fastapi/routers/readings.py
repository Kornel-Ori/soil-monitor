from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

import models
from database import get_db
from schemas import ReadingCreate, ReadingResponse, ReadingUpdate


router = APIRouter(tags=["Readings"])


@router.get("/readings/", response_model=list[ReadingResponse])
def get_all_readings(db: Session = Depends(get_db)):
    result = db.execute(select(models.Reading))
    return result.scalars().all()


@router.get("/plants/{plant_id}/readings", response_model=list[ReadingResponse])
def get_plant_readings(plant_id: int, db: Session = Depends(get_db)):
    plant = db.get(models.Plant, plant_id)

    if plant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plant not found"
        )

    result = db.execute(
        select(models.Reading)
        .join(models.Node)
        .where(models.Node.plant_id == plant_id)
        .order_by(models.Reading.recorded_at.desc())
    )

    return result.scalars().all()


@router.get("/readings/{reading_id}", response_model=ReadingResponse)
def get_reading(reading_id: int, db: Session = Depends(get_db)):
    result = db.get(models.Reading, reading_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reading not found"
        )
    return result


@router.post("/readings/", response_model=ReadingResponse, status_code=status.HTTP_201_CREATED)
def create_new_reading(reading: ReadingCreate, db: Session = Depends(get_db)):
    result = models.Reading(**reading.model_dump())
    db.add(result)
    db.commit()
    db.refresh(result)
    return result


@router.patch("/readings/{reading_id}", response_model=ReadingResponse)
def update_existing_reading(reading_id: int, reading: ReadingUpdate, db: Session = Depends(get_db)):
    result = db.get(models.Reading, reading_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reading not found"
        )
    for key, value in reading.model_dump(exclude_unset=True).items():
        setattr(result, key, value)
    db.commit()
    db.refresh(result)
    return result


@router.delete("/readings/{reading_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_reading(reading_id: int, db: Session = Depends(get_db)):
    result = db.get(models.Reading, reading_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reading not found"
        )
    db.delete(result)
    db.commit()
    return None