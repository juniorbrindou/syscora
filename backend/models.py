import enum
from datetime import datetime, timezone

from sqlalchemy import (
    Boolean, Column, DateTime, Enum as SQLEnum,
    Float, ForeignKey, Integer, String, Text
)
from sqlalchemy.orm import relationship

from database import Base


class RoleEnum(str, enum.Enum):
    ADMIN = "admin"
    COMPTABLE = "comptable"
    MANAGER = "manager"


class TypeCompte(str, enum.Enum):
    CHARGE = "CHARGE"
    PRODUIT = "PRODUIT"
    NEUTRE = "NEUTRE"


class TypeAxe(str, enum.Enum):
    CENTRE_COUT = "CENTRE_COUT"
    PROJET = "PROJET"
    DEPARTEMENT = "DEPARTEMENT"


class SensEcriture(str, enum.Enum):
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"


def _now():
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(200), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(SQLEnum(RoleEnum), default=RoleEnum.COMPTABLE, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=_now, nullable=False)

    ecritures = relationship("EcritureAnalytique", back_populates="user")


class CompteAnalytique(Base):
    __tablename__ = "comptes_analytiques"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, index=True, nullable=False)
    libelle = Column(String(200), nullable=False)
    type = Column(SQLEnum(TypeCompte), default=TypeCompte.CHARGE, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=_now, nullable=False)

    ecritures = relationship("EcritureAnalytique", back_populates="compte")


class AxeAnalytique(Base):
    __tablename__ = "axes_analytiques"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, index=True, nullable=False)
    libelle = Column(String(200), nullable=False)
    type = Column(SQLEnum(TypeAxe), default=TypeAxe.CENTRE_COUT, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=_now, nullable=False)

    ecritures = relationship("EcritureAnalytique", back_populates="axe")


class EcritureAnalytique(Base):
    __tablename__ = "ecritures_analytiques"

    id = Column(Integer, primary_key=True, index=True)
    reference = Column(String(50), unique=True, index=True, nullable=False)
    date_ecriture = Column(DateTime(timezone=True), nullable=False)
    libelle = Column(Text, nullable=False)
    montant = Column(Float, nullable=False)
    sens = Column(SQLEnum(SensEcriture), nullable=False)
    devise = Column(String(3), default="EUR", nullable=False)
    compte_id = Column(Integer, ForeignKey("comptes_analytiques.id"), nullable=False)
    axe_id = Column(Integer, ForeignKey("axes_analytiques.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=_now, nullable=False)

    compte = relationship("CompteAnalytique", back_populates="ecritures")
    axe = relationship("AxeAnalytique", back_populates="ecritures")
    user = relationship("User", back_populates="ecritures")
