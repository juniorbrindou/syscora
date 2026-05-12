// ── Enums ────────────────────────────────────────────────────────────────────

export type Role = 'admin' | 'comptable' | 'manager';
export type TypeCompte = 'CHARGE' | 'PRODUIT' | 'NEUTRE';
export type TypeAxe = 'CENTRE_COUT' | 'PROJET' | 'DEPARTEMENT';
export type SensEcriture = 'DEBIT' | 'CREDIT';

// ── API models ────────────────────────────────────────────────────────────────

export interface User {
  id: number;
  email: string;
  full_name: string;
  role: Role;
  is_active: boolean;
  created_at: string;
}

export interface Token {
  access_token: string;
  token_type: string;
  user: User;
}

export interface CompteAnalytique {
  id: number;
  code: string;
  libelle: string;
  type: TypeCompte;
  is_active: boolean;
  created_at: string;
}

export interface AxeAnalytique {
  id: number;
  code: string;
  libelle: string;
  type: TypeAxe;
  is_active: boolean;
  created_at: string;
}

export interface EcritureAnalytique {
  id: number;
  reference: string;
  date_ecriture: string;
  libelle: string;
  montant: number;
  sens: SensEcriture;
  devise: string;
  compte_id: number;
  axe_id: number;
  user_id: number;
  created_at: string;
  compte?: CompteAnalytique;
  axe?: AxeAnalytique;
}

export interface KPIs {
  total_charges: number;
  total_produits: number;
  resultat: number;
  nb_ecritures: number;
  nb_axes_actifs: number;
}

export interface RepartitionItem {
  axe: string;
  type: string;
  montant: number;
}

export interface EvolutionItem {
  mois: string;
  charges: number;
  produits: number;
}

// ── Request payloads ──────────────────────────────────────────────────────────

export interface LoginRequest {
  email: string;
  password: string;
}

export interface CompteCreateRequest {
  code: string;
  libelle: string;
  type: TypeCompte;
}

export interface AxeCreateRequest {
  code: string;
  libelle: string;
  type: TypeAxe;
}

export interface EcritureCreateRequest {
  date_ecriture: string;
  libelle: string;
  montant: number;
  sens: SensEcriture;
  devise: string;
  compte_id: number;
  axe_id: number;
}
