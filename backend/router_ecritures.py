from datetime import timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload

import models
import schemas
from auth import get_current_user
from database import get_db

router = APIRouter(prefix="/ecritures", tags=["Écritures analytiques"])


def _generate_reference(db: Session) -> str:
    from datetime import datetime
    count = db.query(models.EcritureAnalytique).count()
    date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
    return f"ECR-{date_str}-{count + 1:05d}"


@router.get("", response_model=List[schemas.EcritureResponse])
def list_ecritures(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    compte_id: Optional[int] = None,
    axe_id: Optional[int] = None,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    q = (
        db.query(models.EcritureAnalytique)
        .options(
            joinedload(models.EcritureAnalytique.compte),
            joinedload(models.EcritureAnalytique.axe),
        )
        .order_by(models.EcritureAnalytique.date_ecriture.desc())
    )
    if compte_id is not None:
        q = q.filter(models.EcritureAnalytique.compte_id == compte_id)
    if axe_id is not None:
        q = q.filter(models.EcritureAnalytique.axe_id == axe_id)
    return q.offset(skip).limit(limit).all()


@router.post("", response_model=schemas.EcritureResponse, status_code=201)
def create_ecriture(
    ecriture: schemas.EcritureCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    # Validate compte and axe exist and are active
    compte = db.query(models.CompteAnalytique).filter(
        models.CompteAnalytique.id == ecriture.compte_id,
        models.CompteAnalytique.is_active == True,
    ).first()
    if not compte:
        raise HTTPException(status_code=400, detail="Compte analytique introuvable ou inactif")

    axe = db.query(models.AxeAnalytique).filter(
        models.AxeAnalytique.id == ecriture.axe_id,
        models.AxeAnalytique.is_active == True,
    ).first()
    if not axe:
        raise HTTPException(status_code=400, detail="Axe analytique introuvable ou inactif")

    db_ecriture = models.EcritureAnalytique(
        reference=_generate_reference(db),
        date_ecriture=ecriture.date_ecriture,
        libelle=ecriture.libelle,
        montant=ecriture.montant,
        sens=ecriture.sens,
        devise=ecriture.devise,
        compte_id=ecriture.compte_id,
        axe_id=ecriture.axe_id,
        user_id=current_user.id,
    )
    db.add(db_ecriture)
    db.commit()
    db.refresh(db_ecriture)
    # Reload with relationships
    db.refresh(db_ecriture)
    db_ecriture.compte  # trigger lazy load
    db_ecriture.axe
    return db_ecriture


@router.get("/{ecriture_id}", response_model=schemas.EcritureResponse)
def get_ecriture(
    ecriture_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    ecriture = (
        db.query(models.EcritureAnalytique)
        .options(
            joinedload(models.EcritureAnalytique.compte),
            joinedload(models.EcritureAnalytique.axe),
        )
        .filter(models.EcritureAnalytique.id == ecriture_id)
        .first()
    )
    if not ecriture:
        raise HTTPException(status_code=404, detail="Écriture introuvable")
    return ecriture
