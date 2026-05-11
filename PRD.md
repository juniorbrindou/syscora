# Product Requirements Document (PRD) - Syscora

## 1. Résumé Exécutif
**Syscora** est une application moderne de **comptabilité analytique** conçue pour offrir aux entreprises (de la PME à la grande structure) une vue claire, ventilée et en temps réel de leurs performances financières. Le système permettra l'enregistrement d'écritures comptables, la ventilation analytique multi-axes (projets, centres de coûts), la gestion multi-sociétés et multi-devises, tout en garantissant un haut niveau de conformité, de sécurité et d'auditabilité.

## 2. Objectifs du Projet
*   **Centraliser et automatiser** la répartition analytique des écritures comptables.
*   **Fournir des indicateurs de performance (KPI) en temps réel** via des tableaux de bord interactifs.
*   **Assurer la conformité et la sécurité** des données financières (pistes d'audit immuables, FEC, RGPD).
*   **Garantir la scalabilité** pour accompagner la croissance de l'entreprise (augmentation du volume de données et du nombre d'utilisateurs).

## 3. Choix Technologiques & Architecture
Suite à l'analyse des besoins de scalabilité, de robustesse et de productivité, la stack technologique suivante a été sélectionnée :

| Couche | Technologie Choisie | Justification |
| :--- | :--- | :--- |
| **Frontend** | **Angular** (TypeScript) | Framework robuste, opinionated et extrêmement structuré. Parfaitement adapté aux applications d'entreprise complexes. Utilisation de bibliothèques comme Angular Material ou PrimeNG pour des composants UI riches (grilles de données, formulaires avancés). |
| **Backend** | **FastAPI** (Python) | Très haute performance (grâce à ASGI), typage fort avec Pydantic, génération automatique de la documentation interactive (Swagger/OpenAPI). Très adapté pour construire rapidement des API REST robustes et intégrer facilement des librairies de calculs analytiques Python (Pandas) si besoin. |
| **Base de données (OLTP)** | **PostgreSQL** | Standard open-source pour les données relationnelles complexes et les transactions financières. Support natif du format JSONB pour une flexibilité accrue. |
| **Base de données (OLAP) - Optionnelle** | **ClickHouse** (Évolutif) | Si les volumes de données deviennent très importants pour le reporting, ajout d'une base orientée colonne pour des agrégations ultra-rapides. |
| **ORM & Accès Données** | **SQLAlchemy** / **SQLModel** | ORM mature et robuste pour Python, facilitant l'interaction avec PostgreSQL tout en maintenant des performances élevées. |
| **Visualisation (Dashboards)**| **ECharts** ou **Chart.js** | Intégration facile avec Angular. ECharts offre d'excellentes performances pour les grands jeux de données et une grande variété de visualisations adaptées à la finance. |
| **Authentification & Sécurité** | **Auth0** ou **Keycloak** | Gestion des identités, SSO (Single Sign-On), OAuth2/OpenID Connect. Modèle RBAC (Role-Based Access Control) pour gérer finement les permissions (Admin, Comptable, Manager). |
| **Infrastructure & Déploiement** | **Docker, Kubernetes (K8s), CI/CD** | Conteneurisation de FastAPI et Angular. Déploiement cloud (AWS/GCP/Azure) pour la haute disponibilité. Pipeline CI/CD automatisé (GitHub Actions ou GitLab CI). |

## 4. Périmètre du Produit (Scope) & MVP

### Phase 1 : Le MVP (Minimum Viable Product)
L'objectif du MVP est de valider le socle technique et les fonctionnalités de base de saisie et de restitution.
*   **Authentification et Autorisation :** Connexion sécurisée, gestion des rôles de base.
*   **Paramétrage de base :** Création des plans de comptes analytiques, des centres de coûts et des projets (mono-société et mono-devise pour commencer).
*   **Saisie des écritures :** Formulaire de saisie d'écritures analytiques avec contrôles de validation (équilibre des montants, affectation obligatoire).
*   **Reporting basique :** Balance analytique simple et un tableau de bord (répartition des coûts par centre de coûts/projets).

### Phase 2 : Évolutions post-MVP
*   **Multi-sociétés & Multi-devises :** Gestion des filiales, taux de change, consolidation.
*   **Import/Export & Intégration :** API d'intégration avec la comptabilité générale, import de fichiers CSV/Excel.
*   **Règles de répartition automatiques :** Moteur d'allocation pour automatiser la ventilation des frais généraux.
*   **Budget et Prévisions :** Saisie des budgets et analyse des écarts réel vs budget.

## 5. Exigences Fonctionnelles
1.  **Ventilation Analytique :** Imputation des montants sur un ou plusieurs axes analytiques (projets, départements).
2.  **Plan Analytique Dynamique :** Possibilité de créer des hiérarchies de centres de coûts et de projets.
3.  **Auditabilité :** Toutes les actions (créations, modifications, suppressions logiques) doivent être historisées avec l'utilisateur et la date (Piste d'audit).
4.  **Tableaux de bord (Dashboards) :** Visualisations interactives filtrables par date, centre de coûts, projet, société.
5.  **Multi-Tenant / Multi-Sociétés :** Séparation stricte des données entre les différentes sociétés configurées, avec possibilité de consolidation.

## 6. Exigences Non-Fonctionnelles
1.  **Performance :** L'API FastAPI doit répondre en moins de 200ms pour les requêtes standard. Les rapports lourds seront gérés asynchroniquement si nécessaire (ex: via Celery ou BackgroundTasks).
2.  **Sécurité :** Chiffrement des données en transit (HTTPS/TLS) et au repos. Protection contre les vulnérabilités OWASP (gérée par les frameworks choisis).
3.  **Disponibilité :** Architecture cloud tolérante aux pannes (redondance base de données, load balancing).
4.  **Conformité :** Conformité RGPD pour les données utilisateurs, et préparation pour les normes fiscales (FEC).

## 7. Modèle de Données Simplifié (Entités Principales)
*   **Tenant / Societe :** L'entité légale ou le sous-groupe.
*   **CompteAnalytique :** Définition de la nature de la charge ou du produit.
*   **AxeAnalytique (Centre de Cout / Projet) :** La destination de la charge.
*   **EcritureAnalytique :** La transaction financière ventilée (Date, Montant, Devise, Utilisateur, Liens vers Compte et Axes).
*   **Utilisateur & Role :** Pour l'accès et les permissions.

## 8. Roadmap & Planning Prévisionnel (Basé sur le Rapport)
*   **Mois 1 :** Architecture logicielle, configuration DevOps (Docker, CI/CD), setup des dépôts Angular et FastAPI. Conception détaillée de la BDD.
*   **Mois 2 :** Implémentation de l'authentification (Keycloak/Auth0), CRUD de base pour le paramétrage (Comptes, Centres, Projets).
*   **Mois 3 :** Moteur de saisie des écritures (Backend & Frontend).
*   **Mois 4 :** Tableaux de bord (intégration ECharts/Chart.js) et rapports d'exports.
*   **Fin du Mois 4 :** Livraison du **MVP**.
*   **Mois 5-6 :** Développements Phase 2 (Multi-devises, Règles de répartition automatique, Intégration comptabilité générale).
