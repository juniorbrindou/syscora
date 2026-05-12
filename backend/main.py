from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import models
from auth import hash_password
from database import Base, SessionLocal, engine
from router_auth import router as auth_router
from router_axes import router as axes_router
from router_comptes import router as comptes_router
from router_dashboard import router as dashboard_router
from router_ecritures import router as ecritures_router


def _seed_db():
    """Create tables and seed initial admin user + demo data."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Admin user
        if not db.query(models.User).first():
            admin = models.User(
                email="admin@syscora.com",
                full_name="Administrateur Syscora",
                hashed_password=hash_password("Admin@2024"),
                role=models.RoleEnum.ADMIN,
            )
            db.add(admin)
            db.flush()

            # Demo comptes
            comptes_data = [
                ("601000", "Achats de marchandises", models.TypeCompte.CHARGE),
                ("621000", "Personnel extérieur", models.TypeCompte.CHARGE),
                ("626000", "Frais postaux et télécom", models.TypeCompte.CHARGE),
                ("641000", "Rémunérations du personnel", models.TypeCompte.CHARGE),
                ("701000", "Ventes de produits finis", models.TypeCompte.PRODUIT),
                ("706000", "Prestations de services", models.TypeCompte.PRODUIT),
            ]
            comptes = []
            for code, libelle, typ in comptes_data:
                c = models.CompteAnalytique(code=code, libelle=libelle, type=typ)
                db.add(c)
                comptes.append(c)
            db.flush()

            # Demo axes
            axes_data = [
                ("CC-IT", "Centre IT & Infra", models.TypeAxe.CENTRE_COUT),
                ("CC-MKT", "Marketing & Com", models.TypeAxe.CENTRE_COUT),
                ("CC-RH", "Ressources Humaines", models.TypeAxe.CENTRE_COUT),
                ("PRJ-ALPHA", "Projet Alpha", models.TypeAxe.PROJET),
                ("PRJ-BETA", "Projet Beta", models.TypeAxe.PROJET),
                ("DEPT-FINANCE", "Direction Financière", models.TypeAxe.DEPARTEMENT),
            ]
            axes = []
            for code, libelle, typ in axes_data:
                a = models.AxeAnalytique(code=code, libelle=libelle, type=typ)
                db.add(a)
                axes.append(a)
            db.flush()

            # Demo écritures
            from datetime import datetime, timezone
            demo_ecritures = [
                (datetime(2026, 1, 15, tzinfo=timezone.utc), "Achat matériel IT", 12500.00, models.SensEcriture.DEBIT, comptes[0], axes[0]),
                (datetime(2026, 2, 3, tzinfo=timezone.utc), "Campagne LinkedIn", 3200.00, models.SensEcriture.DEBIT, comptes[1], axes[1]),
                (datetime(2026, 2, 28, tzinfo=timezone.utc), "Salaires Fév 2026", 45000.00, models.SensEcriture.DEBIT, comptes[3], axes[2]),
                (datetime(2026, 3, 10, tzinfo=timezone.utc), "Prestation client A", 28000.00, models.SensEcriture.CREDIT, comptes[5], axes[3]),
                (datetime(2026, 3, 20, tzinfo=timezone.utc), "Frais télécom Mars", 850.00, models.SensEcriture.DEBIT, comptes[2], axes[0]),
                (datetime(2026, 4, 5, tzinfo=timezone.utc), "Vente produit B", 15000.00, models.SensEcriture.CREDIT, comptes[4], axes[4]),
                (datetime(2026, 4, 30, tzinfo=timezone.utc), "Salaires Avr 2026", 47000.00, models.SensEcriture.DEBIT, comptes[3], axes[2]),
                (datetime(2026, 5, 2, tzinfo=timezone.utc), "Mission conseil externe", 6500.00, models.SensEcriture.DEBIT, comptes[1], axes[5]),
                (datetime(2026, 5, 8, tzinfo=timezone.utc), "Prestation client B", 32000.00, models.SensEcriture.CREDIT, comptes[5], axes[3]),
            ]
            for i, (date, libelle, montant, sens, compte, axe) in enumerate(demo_ecritures, start=1):
                e = models.EcritureAnalytique(
                    reference=f"ECR-{date.strftime('%Y%m%d')}-{i:05d}",
                    date_ecriture=date,
                    libelle=libelle,
                    montant=montant,
                    sens=sens,
                    devise="EUR",
                    compte_id=compte.id,
                    axe_id=axe.id,
                    user_id=admin.id,
                )
                db.add(e)

            db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    _seed_db()
    yield


app = FastAPI(
    title="Syscora API",
    description="API de comptabilité analytique Syscora",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_PREFIX = "/api"
app.include_router(auth_router, prefix=API_PREFIX)
app.include_router(comptes_router, prefix=API_PREFIX)
app.include_router(axes_router, prefix=API_PREFIX)
app.include_router(ecritures_router, prefix=API_PREFIX)
app.include_router(dashboard_router, prefix=API_PREFIX)


@app.get("/")
def root():
    return {"message": "Syscora API v1.0", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}
