# Design System & UI/UX Guidelines - Syscora

## 1. Vision & Identité Visuelle
L'interface de Syscora est pensée à la croisée de la **Fintech moderne (type Stripe)** et du **Minimalisme utilitaire (type Linear/Shadcn)**.
L'objectif est d'inspirer la confiance (données financières) tout en permettant à l'utilisateur de traiter une haute densité d'informations (tableaux comptables, écritures) sans fatigue visuelle.

**Mots-clés :** Professionnel, Épuré, Aéré, Haute lisibilité, Rapide.

---

## 2. Typographie
Pour garantir une lecture optimale des chiffres et une hiérarchie claire, nous utilisons une typographie moderne, géométrique et sans-serif.

*   **Police Principale :** `Inter` (Google Fonts)
*   **Police Monospace (pour les montants/codes analytiques) :** `JetBrains Mono` ou `Roboto Mono`

**Échelle Typographique :**
*   `h1` (Titres de pages) : 24px, Font-weight: 700 (Bold), Letter-spacing: -2%
*   `h2` (Titres de sections/cartes) : 18px, Font-weight: 600 (Semi-bold)
*   `Body` (Texte standard) : 14px, Font-weight: 400 (Regular)
*   `Small` (Labels, légendes) : 12px, Font-weight: 500 (Medium)

---

## 3. Palette de Couleurs
La palette privilégie des fonds clairs (ou sombres très profonds en Dark Mode) avec des contrastes nets pour les données, et des couleurs d'accentuation subtiles.

### Mode Clair (Light Mode - Par défaut)
*   **Fonds (Backgrounds) :**
    *   Fond de l'application : `#F9FAFB` (Gris très léger)
    *   Fond des cartes/composants : `#FFFFFF` (Blanc pur)
*   **Texte :**
    *   Texte principal : `#111827` (Noir profond)
    *   Texte secondaire / Labels : `#6B7280` (Gris ardoise)
*   **Bordures & Lignes (Séparateurs) :** `#E5E7EB` (Gris clair, très fin, 1px)
*   **Couleur Primaire (Actions, Boutons, Liens) :** `#6366F1` (Indigo - *Confiance & Modernité*) ou `#0F172A` (Bleu nuit très sombre - *Sobriété*)
*   **Couleurs Sémantiques (États & Montants) :**
    *   Succès / Crédit : `#10B981` (Vert émeraude)
    *   Danger / Débit / Erreur : `#EF4444` (Rouge vif)
    *   Avertissement : `#F59E0B` (Ambre)

---

## 4. Composants UI (Éléments d'interface)

### Boutons
*   **Primaire :** Fond Indigo ou Noir, texte blanc, pas de bordure, très léger hover effect (assombrissement). Border-radius: `6px`.
*   **Secondaire :** Fond blanc, bordure 1px gris clair, texte noir. Idéal pour les actions comme "Annuler" ou "Filtrer".
*   **Ghost (Tertiaire) :** Pas de fond, pas de bordure, le fond devient gris très clair au survol.

### Formulaires & Saisie (Inputs)
*   **Design :** Minimaliste. Fond blanc, bordure 1px grise (`#D1D5DB`). Focus state net : bordure Indigo 2px, pas d'ombre (ou une ombre très légère).
*   **Labels :** Petits (12px), placés au-dessus du champ, couleur gris ardoise.
*   **Alignement :** Les champs contenant des montants financiers (devises) doivent toujours être alignés à **droite**.

### Cartes (Cards) & Conteneurs
*   Les cartes englobent les graphiques ou les sections de paramétrage.
*   **Style :** Fond blanc, bordure 1px gris très clair (`#E5E7EB`), **pas d'ombre** (flat design) ou une ombre extrêmement subtile (`box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05)`).
*   Border-radius : `8px`.

---

## 5. Tableaux de Données (Data Grids)
C'est le cœur de l'application (liste des écritures, balances).
*   **Densité :** Haute. L'espace vertical (padding) dans les cellules doit être réduit (ex: 8px ou 12px) pour afficher un maximum de lignes.
*   **Bordures :** Lignes de séparation horizontales uniquement (très claires). Pas de bordures verticales entre les colonnes pour alléger la vue.
*   **Interactivité :** Légère surbrillance de la ligne entière (row hover) en gris très clair (`#F3F4F6`).
*   **Zebra-striping :** Facultatif, à utiliser uniquement si les colonnes sont très larges.

---

## 6. Graphiques & Data Visualization (ECharts / Chart.js)
*   **Style des graphiques :** Lignes épurées, pas de remplissage avec des dégradés lourds. Utilisation de lignes lisses (smooth curves).
*   **Tooltips (Bulle d'info) :** Fond noir/sombre, texte blanc, apparition rapide sans animation lourde. Affichage du montant formaté avec la devise.
*   **Couleurs des séries :** Utiliser des palettes harmonieuses (Indigo, Bleu ciel, Violet) plutôt que des couleurs primaires basiques.

---

## 7. Espacements & Grille (Layout)
*   **Système d'espacement :** Base 4px ou 8px (ex: margins/paddings de 8, 16, 24, 32px).
*   **Menu (Sidebar) :** Verticale, à gauche, avec des icônes fines (ex: Lucide Icons ou Heroicons) et un fond sombre (`#111827`) ou très clair (`#FFFFFF`) avec une bordure droite.
*   **Header :** Discret, contenant le fil d'ariane (Breadcrumb), le sélecteur de société (Company/Tenant switcher) et le profil utilisateur.
