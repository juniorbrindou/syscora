import { Component, OnInit, inject, signal } from '@angular/core';
import { DatePipe, NgClass } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { ApiService } from '../../services/api.service';
import { AxeAnalytique, CompteAnalytique, EcritureAnalytique } from '../../models';

@Component({
  selector: 'app-ecritures',
  standalone: true,
  imports: [ReactiveFormsModule, DatePipe, NgClass],
  templateUrl: './ecritures.html',
  styleUrl: './ecritures.css',
})
export class EcrituresPage implements OnInit {
  private api = inject(ApiService);
  private fb = inject(FormBuilder);

  ecritures = signal<EcritureAnalytique[]>([]);
  comptes = signal<CompteAnalytique[]>([]);
  axes = signal<AxeAnalytique[]>([]);
  showForm = signal(false);
  submitting = signal(false);
  error = signal('');
  success = signal('');

  form = this.fb.group({
    date_ecriture: ['', Validators.required],
    libelle: ['', [Validators.required, Validators.maxLength(500)]],
    montant: [null as number | null, [Validators.required, Validators.min(0.01)]],
    sens: ['DEBIT', Validators.required],
    devise: ['EUR', [Validators.required, Validators.minLength(3), Validators.maxLength(3)]],
    compte_id: [null as number | null, Validators.required],
    axe_id: [null as number | null, Validators.required],
  });

  ngOnInit(): void {
    this.loadAll();
  }

  loadAll(): void {
    this.api.getEcritures().subscribe((e) => this.ecritures.set(e));
    this.api.getComptes().subscribe((c) => this.comptes.set(c.filter((x) => x.is_active)));
    this.api.getAxes().subscribe((a) => this.axes.set(a.filter((x) => x.is_active)));
  }

  toggleForm(): void {
    this.showForm.update((v) => !v);
    if (!this.showForm()) {
      this.form.reset({ sens: 'DEBIT', devise: 'EUR' });
      this.error.set('');
      this.success.set('');
    }
  }

  submit(): void {
    if (this.form.invalid) return;
    this.submitting.set(true);
    this.error.set('');
    this.success.set('');

    const v = this.form.value;
    // Ensure ISO date format
    const dateStr = v.date_ecriture
      ? new Date(v.date_ecriture).toISOString()
      : '';

    const payload = {
      date_ecriture: dateStr,
      libelle: v.libelle!,
      montant: Number(v.montant),
      sens: v.sens as 'DEBIT' | 'CREDIT',
      devise: (v.devise || 'EUR').toUpperCase(),
      compte_id: Number(v.compte_id),
      axe_id: Number(v.axe_id),
    };

    this.api.createEcriture(payload).subscribe({
      next: (e) => {
        this.success.set(`Écriture ${e.reference} enregistrée avec succès.`);
        this.form.reset({ sens: 'DEBIT', devise: 'EUR' });
        this.submitting.set(false);
        this.api.getEcritures().subscribe((list) => this.ecritures.set(list));
      },
      error: (err) => {
        this.error.set(err.error?.detail ?? 'Erreur lors de l\'enregistrement');
        this.submitting.set(false);
      },
    });
  }

  formatMontant(value: number, sens: string): string {
    const formatted = value.toLocaleString('fr-FR', { minimumFractionDigits: 2 });
    return sens === 'DEBIT' ? `- ${formatted}` : `+ ${formatted}`;
  }

  sensBadge(sens: string): string {
    return sens === 'DEBIT' ? 'badge--danger' : 'badge--success';
  }
}
