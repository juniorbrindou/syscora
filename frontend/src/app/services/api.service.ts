import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import {
  AxeAnalytique,
  AxeCreateRequest,
  CompteAnalytique,
  CompteCreateRequest,
  EcritureAnalytique,
  EcritureCreateRequest,
  EvolutionItem,
  KPIs,
  RepartitionItem,
  Token,
} from '../models';

const API = '/api';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private http = inject(HttpClient);

  // ── Auth ──────────────────────────────────────────────────────────────────

  login(email: string, password: string): Observable<Token> {
    return this.http.post<Token>(`${API}/auth/login`, { email, password });
  }

  // ── Comptes analytiques ───────────────────────────────────────────────────

  getComptes(): Observable<CompteAnalytique[]> {
    return this.http.get<CompteAnalytique[]>(`${API}/comptes`);
  }

  createCompte(payload: CompteCreateRequest): Observable<CompteAnalytique> {
    return this.http.post<CompteAnalytique>(`${API}/comptes`, payload);
  }

  updateCompte(id: number, payload: Partial<CompteCreateRequest & { is_active: boolean }>): Observable<CompteAnalytique> {
    return this.http.put<CompteAnalytique>(`${API}/comptes/${id}`, payload);
  }

  deleteCompte(id: number): Observable<void> {
    return this.http.delete<void>(`${API}/comptes/${id}`);
  }

  // ── Axes analytiques ──────────────────────────────────────────────────────

  getAxes(): Observable<AxeAnalytique[]> {
    return this.http.get<AxeAnalytique[]>(`${API}/axes`);
  }

  createAxe(payload: AxeCreateRequest): Observable<AxeAnalytique> {
    return this.http.post<AxeAnalytique>(`${API}/axes`, payload);
  }

  updateAxe(id: number, payload: Partial<AxeCreateRequest & { is_active: boolean }>): Observable<AxeAnalytique> {
    return this.http.put<AxeAnalytique>(`${API}/axes/${id}`, payload);
  }

  deleteAxe(id: number): Observable<void> {
    return this.http.delete<void>(`${API}/axes/${id}`);
  }

  // ── Écritures analytiques ─────────────────────────────────────────────────

  getEcritures(skip = 0, limit = 50, compteId?: number, axeId?: number): Observable<EcritureAnalytique[]> {
    let params = new HttpParams().set('skip', skip).set('limit', limit);
    if (compteId != null) params = params.set('compte_id', compteId);
    if (axeId != null) params = params.set('axe_id', axeId);
    return this.http.get<EcritureAnalytique[]>(`${API}/ecritures`, { params });
  }

  createEcriture(payload: EcritureCreateRequest): Observable<EcritureAnalytique> {
    return this.http.post<EcritureAnalytique>(`${API}/ecritures`, payload);
  }

  // ── Dashboard ─────────────────────────────────────────────────────────────

  getKPIs(): Observable<KPIs> {
    return this.http.get<KPIs>(`${API}/dashboard/kpis`);
  }

  getRepartition(): Observable<RepartitionItem[]> {
    return this.http.get<RepartitionItem[]>(`${API}/dashboard/repartition`);
  }

  getEvolution(): Observable<EvolutionItem[]> {
    return this.http.get<EvolutionItem[]>(`${API}/dashboard/evolution`);
  }
}
