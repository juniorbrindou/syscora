from collections import defaultdict
from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import models
import schemas
from auth import get_current_user
from database import get_db

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/kpis", response_model=schemas.KPIResponse)
def get_kpis(db: Session = Depends(get_db), _=Depends(get_current_user)):
    ecritures = db.query(models.EcritureAnalytique).all()

    total_charges = 0.0
    total_produits = 0.0

    for e in ecritures:
        compte = db.query(models.CompteAnalytique).filter(models.CompteAnalytique.id == e.compte_id).first()
        if not compte:
            continue
        montant = e.montant if e.sens == models.SensEcriture.DEBIT else -e.montant
        if compte.type == models.TypeCompte.CHARGE:
            total_charges += montant
        elif compte.type == models.TypeCompte.PRODUIT:
            total_produits += abs(montant) if e.sens == models.SensEcriture.CREDIT else -montant

    nb_axes_actifs = db.query(models.AxeAnalytique).filter(models.AxeAnalytique.is_active == True).count()

    return schemas.KPIResponse(
        total_charges=round(total_charges, 2),
        total_produits=round(total_produits, 2),
        resultat=round(total_produits - total_charges, 2),
        nb_ecritures=len(ecritures),
        nb_axes_actifs=nb_axes_actifs,
    )


@router.get("/repartition", response_model=List[schemas.RepartitionItem])
def get_repartition(db: Session = Depends(get_db), _=Depends(get_current_user)):
    """Répartition des montants par axe analytique."""
    ecritures = (
        db.query(models.EcritureAnalytique)
        .join(models.AxeAnalytique, models.EcritureAnalytique.axe_id == models.AxeAnalytique.id)
        .all()
    )

    aggregation: dict[int, dict] = defaultdict(lambda: {"libelle": "", "type": "", "montant": 0.0})
    for e in ecritures:
        axe = db.query(models.AxeAnalytique).filter(models.AxeAnalytique.id == e.axe_id).first()
        if not axe:
            continue
        aggregation[e.axe_id]["libelle"] = axe.libelle
        aggregation[e.axe_id]["type"] = axe.type.value
        aggregation[e.axe_id]["montant"] += e.montant

    return [
        schemas.RepartitionItem(axe=v["libelle"], type=v["type"], montant=round(v["montant"], 2))
        for v in aggregation.values()
        if v["montant"] > 0
    ]


@router.get("/evolution", response_model=List[schemas.EvolutionItem])
def get_evolution(db: Session = Depends(get_db), _=Depends(get_current_user)):
    """Évolution mensuelle des charges et produits sur les 12 derniers mois."""
    from calendar import month_abbr

    ecritures = db.query(models.EcritureAnalytique).all()

    monthly: dict[str, dict[str, float]] = defaultdict(lambda: {"charges": 0.0, "produits": 0.0})

    for e in ecritures:
        compte = db.query(models.CompteAnalytique).filter(models.CompteAnalytique.id == e.compte_id).first()
        if not compte:
            continue
        key = e.date_ecriture.strftime("%Y-%m")
        if compte.type == models.TypeCompte.CHARGE:
            monthly[key]["charges"] += e.montant
        elif compte.type == models.TypeCompte.PRODUIT:
            monthly[key]["produits"] += e.montant

    # Return last 12 months sorted
    sorted_months = sorted(monthly.keys())[-12:]
    result = []
    for key in sorted_months:
        year, month = key.split("-")
        label = f"{month_abbr[int(month)]} {year}"
        result.append(
            schemas.EvolutionItem(
                mois=label,
                charges=round(monthly[key]["charges"], 2),
                produits=round(monthly[key]["produits"], 2),
            )
        )
    return result
