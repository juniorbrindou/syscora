from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
from auth import get_current_user
from database import get_db

router = APIRouter(prefix="/axes", tags=["Axes analytiques"])


@router.get("", response_model=List[schemas.AxeResponse])
def list_axes(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(models.AxeAnalytique).order_by(models.AxeAnalytique.code).all()


@router.post("", response_model=schemas.AxeResponse, status_code=201)
def create_axe(
    axe: schemas.AxeCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    if db.query(models.AxeAnalytique).filter(models.AxeAnalytique.code == axe.code).first():
        raise HTTPException(status_code=400, detail="Ce code d'axe est déjà utilisé")
    db_axe = models.AxeAnalytique(**axe.model_dump())
    db.add(db_axe)
    db.commit()
    db.refresh(db_axe)
    return db_axe


@router.put("/{axe_id}", response_model=schemas.AxeResponse)
def update_axe(
    axe_id: int,
    axe: schemas.AxeUpdate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    db_axe = db.query(models.AxeAnalytique).filter(models.AxeAnalytique.id == axe_id).first()
    if not db_axe:
        raise HTTPException(status_code=404, detail="Axe introuvable")
    for field, value in axe.model_dump(exclude_none=True).items():
        setattr(db_axe, field, value)
    db.commit()
    db.refresh(db_axe)
    return db_axe


@router.delete("/{axe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_axe(
    axe_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    db_axe = db.query(models.AxeAnalytique).filter(models.AxeAnalytique.id == axe_id).first()
    if not db_axe:
        raise HTTPException(status_code=404, detail="Axe introuvable")
    db_axe.is_active = False
    db.commit()
