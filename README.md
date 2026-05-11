# Syscora

## 🚀 La Comptabilité Analytique Réinventée

**Syscora** est une application moderne de comptabilité analytique conçue pour offrir aux entreprises (de la PME à la grande structure) une vue claire, ventilée et en temps réel de leurs performances financières. 

Ce système centralise l'enregistrement d'écritures comptables, automatise la ventilation analytique multi-axes (projets, centres de coûts), gère les contextes multi-sociétés et multi-devises, tout en garantissant un haut niveau de conformité fiscale (FEC), de sécurité et d'auditabilité.

---

## 🛠️ Stack Technologique

Le projet s'appuie sur une architecture robuste, évolutive et moderne :

*   **Frontend :** Angular (TypeScript) avec des bibliothèques de composants riches et de visualisation de données (ECharts / Chart.js).
*   **Backend :** FastAPI (Python) offrant des performances très élevées et une documentation interactive automatique.
*   **Base de Données Principale (OLTP) :** PostgreSQL, pour la gestion robuste des données relationnelles, transactionnelles et la piste d'audit.
*   **ORM :** SQLAlchemy (ou SQLModel) pour interagir efficacement avec PostgreSQL.
*   **Authentification & IAM :** Keycloak ou Auth0 (Gestion des rôles et des identités).
*   **Déploiement & DevOps :** Docker, Kubernetes (K8s) et intégration/déploiement continu (CI/CD).

---

## 📁 Structure du Projet

```text
syscora/
├── backend/            # Code source de l'API (FastAPI) (À créer)
├── frontend/           # Code source de l'application cliente (Angular) (À créer)
├── www/                # Démonstration / Landing page du projet
├── docs/               # Documentation détaillée (Architecture, Modèles de données, API)
├── PRD.md              # Product Requirements Document (Spécifications)
└── README.md           # Ce fichier
```

---

## 🚀 Démarrage Rapide (Développement Local)

*(Note: Ces instructions seront fonctionnelles une fois les dossiers backend et frontend initialisés)*

### Prérequis
*   [Docker](https://www.docker.com/) & Docker Compose
*   [Node.js](https://nodejs.org/) (pour le développement frontend local)
*   [Python 3.11+](https://www.python.org/) (pour le développement backend local)

### Lancer l'environnement de développement complet (via Docker)

1.  Clonez le dépôt :
    ```bash
    git clone <votre-url-de-depot>
    cd syscora
    ```

2.  Copiez les fichiers d'environnement de développement :
    ```bash
    cp .env.example .env
    ```

3.  Démarrez les services avec Docker Compose :
    ```bash
    docker-compose up -d --build
    ```
    *Ceci lancera la base de données PostgreSQL, le backend FastAPI et le frontend Angular.*

### Accès aux services locaux
*   **Application Web (Angular) :** `http://localhost:4200`
*   **API (FastAPI) :** `http://localhost:8000`
*   **Documentation de l'API (Swagger UI) :** `http://localhost:8000/docs`

---

## 🗺️ Roadmap (MVP)

La phase 1 du projet (MVP) inclut :
- [ ] Authentification et gestion des rôles (Comptable, Manager, Admin).
- [ ] Paramétrage des plans analytiques (Axes, Centres de coûts, Projets).
- [ ] Saisie et validation des écritures comptables avec piste d'audit.
- [ ] Reporting de base (Balance analytique, tableau de bord simple).

*Consultez le fichier [PRD.md](./PRD.md) pour les détails complets du périmètre et des évolutions futures.*

---

## 🔒 Sécurité et Conformité

Syscora intègre "by design" la sécurité et les obligations de conformité :
*   Historisation immuable de toute action (Piste d'audit).
*   Chiffrement de bout en bout et des données sensibles en base.
*   Conformité au RGPD (anonymisation, cycle de vie de la donnée).
*   Préparation aux normes fiscales (Fichier des Écritures Comptables - FEC).
