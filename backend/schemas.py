from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator

from models import RoleEnum, SensEcriture, TypeAxe, TypeCompte


# ── Auth ──────────────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    email: str
    password: str


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    role: RoleEnum = RoleEnum.COMPTABLE


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: RoleEnum
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# ── Comptes analytiques ───────────────────────────────────────────────────────

class CompteCreate(BaseModel):
    code: str
    libelle: str
    type: TypeCompte = TypeCompte.CHARGE


class CompteUpdate(BaseModel):
    code: Optional[str] = None
    libelle: Optional[str] = None
    type: Optional[TypeCompte] = None
    is_active: Optional[bool] = None


class CompteResponse(BaseModel):
    id: int
    code: str
    libelle: str
    type: TypeCompte
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Axes analytiques ──────────────────────────────────────────────────────────

class AxeCreate(BaseModel):
    code: str
    libelle: str
    type: TypeAxe = TypeAxe.CENTRE_COUT


class AxeUpdate(BaseModel):
    code: Optional[str] = None
    libelle: Optional[str] = None
    type: Optional[TypeAxe] = None
    is_active: Optional[bool] = None


class AxeResponse(BaseModel):
    id: int
    code: str
    libelle: str
    type: TypeAxe
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Écritures analytiques ─────────────────────────────────────────────────────

class EcritureCreate(BaseModel):
    date_ecriture: datetime
    libelle: str
    montant: float
    sens: SensEcriture
    devise: str = "EUR"
    compte_id: int
    axe_id: int

    @field_validator("montant")
    @classmethod
    def montant_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Le montant doit être strictement positif")
        return round(v, 2)

    @field_validator("devise")
    @classmethod
    def devise_upper(cls, v: str) -> str:
        v = v.strip().upper()
        if len(v) != 3:
            raise ValueError("La devise doit être un code ISO 3 lettres (ex: EUR)")
        return v


class EcritureResponse(BaseModel):
    id: int
    reference: str
    date_ecriture: datetime
    libelle: str
    montant: float
    sens: SensEcriture
    devise: str
    compte_id: int
    axe_id: int
    user_id: int
    created_at: datetime
    compte: Optional[CompteResponse] = None
    axe: Optional[AxeResponse] = None

    model_config = {"from_attributes": True}


# ── Dashboard ─────────────────────────────────────────────────────────────────

class KPIResponse(BaseModel):
    total_charges: float
    total_produits: float
    resultat: float
    nb_ecritures: int
    nb_axes_actifs: int


class RepartitionItem(BaseModel):
    axe: str
    type: str
    montant: float


class EvolutionItem(BaseModel):
    mois: str
    charges: float
    produits: float
