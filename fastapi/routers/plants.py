
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

import models
from database import get_db
from schemas import PlantCreate, PlantResponse, PlantUpdate


router = APIRouter(prefix="/plants", tags=["Plants"])


@router.get("/", response_model=list[PlantResponse])
def get_all_plants(db: Session = Depends(get_db)):
    result = db.execute(select(models.Plant))
    return result.scalars().all()


@router.get("/{plant_id}", response_model=PlantResponse)
def get_plant(plant_id: int, db: Session = Depends(get_db)):
    result = db.get(models.Plant, plant_id)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plant not found"
        )

    return result


@router.post("/", response_model=PlantResponse, status_code=status.HTTP_201_CREATED)
def create_new_plant(plant: PlantCreate, db: Session = Depends(get_db)):
    result = models.Plant(**plant.model_dump())
    db.add(result)
    db.commit()
    db.refresh(result)
    return result


@router.patch("/{plant_id}", response_model=PlantResponse)
def update_existing_plant(plant_id: int, plant: PlantUpdate, db: Session = Depends(get_db)):
    result = db.get(models.Plant, plant_id)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plant not found"
        )

    for key, value in plant.model_dump(exclude_unset=True).items():
        setattr(result, key, value)

    db.commit()
    db.refresh(result)
    return result


@router.delete("/{plant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_plant(plant_id: int, db: Session = Depends(get_db)):
    result = db.get(models.Plant, plant_id)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plant not found"
        )

    db.delete(result)
    db.commit()
    return None
