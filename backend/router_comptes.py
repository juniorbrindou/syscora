from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
from auth import get_current_user
from database import get_db

router = APIRouter(prefix="/comptes", tags=["Comptes analytiques"])


@router.get("", response_model=List[schemas.CompteResponse])
def list_comptes(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(models.CompteAnalytique).order_by(models.CompteAnalytique.code).all()


@router.post("", response_model=schemas.CompteResponse, status_code=201)
def create_compte(
    compte: schemas.CompteCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    if db.query(models.CompteAnalytique).filter(models.CompteAnalytique.code == compte.code).first():
        raise HTTPException(status_code=400, detail="Ce code de compte est déjà utilisé")
    db_compte = models.CompteAnalytique(**compte.model_dump())
    db.add(db_compte)
    db.commit()
    db.refresh(db_compte)
    return db_compte


@router.put("/{compte_id}", response_model=schemas.CompteResponse)
def update_compte(
    compte_id: int,
    compte: schemas.CompteUpdate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    db_compte = db.query(models.CompteAnalytique).filter(models.CompteAnalytique.id == compte_id).first()
    if not db_compte:
        raise HTTPException(status_code=404, detail="Compte introuvable")
    for field, value in compte.model_dump(exclude_none=True).items():
        setattr(db_compte, field, value)
    db.commit()
    db.refresh(db_compte)
    return db_compte


@router.delete("/{compte_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_compte(
    compte_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    db_compte = db.query(models.CompteAnalytique).filter(models.CompteAnalytique.id == compte_id).first()
    if not db_compte:
        raise HTTPException(status_code=404, detail="Compte introuvable")
    db_compte.is_active = False
    db.commit()
