from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

import models
from database import get_db
from schemas import NodeCreate, NodeResponse


router = APIRouter(prefix="/nodes", tags=["Nodes"])


@router.get("/", response_model=list[NodeResponse])
def get_all_nodes(db: Session = Depends(get_db)):
    result = db.execute(select(models.Node))
    return result.scalars().all()


@router.get("/{node_id}", response_model=NodeResponse)
def get_node(node_id: int, db: Session = Depends(get_db)):
    result = db.get(models.Node, node_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Node not found"
        )
    return result


@router.post("/", response_model=NodeResponse, status_code=status.HTTP_201_CREATED)
def create_new_node(node: NodeCreate, db: Session = Depends(get_db)):
    result = models.Node(**node.model_dump())
    db.add(result)
    db.commit()
    db.refresh(result)
    return result


@router.patch("/{node_id}", response_model=NodeResponse)
def update_existing_node(node_id: int, node: NodeCreate, db: Session = Depends(get_db)):
    result = db.get(models.Node, node_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Node not found"
        )
    for key, value in node.model_dump(exclude_unset=True).items():
        setattr(result, key, value)
    db.commit()
    db.refresh(result)
    return result


@router.delete("/{node_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_node(node_id: int, db: Session = Depends(get_db)):
    result = db.get(models.Node, node_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Node not found"
        )
    db.delete(result)
    db.commit()
    return None