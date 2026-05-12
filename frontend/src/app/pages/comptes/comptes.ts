import { Component, OnInit, inject, signal } from '@angular/core';
import { NgClass } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { ApiService } from '../../services/api.service';
import { CompteAnalytique, TypeCompte } from '../../models';

@Component({
  selector: 'app-comptes',
  standalone: true,
  imports: [ReactiveFormsModule, NgClass],
  templateUrl: './comptes.html',
  styleUrl: './comptes.css',
})
export class ComptesPage implements OnInit {
  private api = inject(ApiService);
  private fb = inject(FormBuilder);

  comptes = signal<CompteAnalytique[]>([]);
  showModal = signal(false);
  editId = signal<number | null>(null);
  submitting = signal(false);
  error = signal('');

  readonly typeOptions: { value: TypeCompte; label: string }[] = [
    { value: 'CHARGE', label: 'Charge' },
    { value: 'PRODUIT', label: 'Produit' },
    { value: 'NEUTRE', label: 'Neutre' },
  ];

  form = this.fb.group({
    code: ['', [Validators.required, Validators.maxLength(20)]],
    libelle: ['', [Validators.required, Validators.maxLength(200)]],
    type: ['CHARGE' as TypeCompte, Validators.required],
  });

  ngOnInit(): void {
    this.load();
  }

  load(): void {
    this.api.getComptes().subscribe((c) => this.comptes.set(c));
  }

  openCreate(): void {
    this.editId.set(null);
    this.form.reset({ code: '', libelle: '', type: 'CHARGE' });
    this.error.set('');
    this.showModal.set(true);
  }

  openEdit(c: CompteAnalytique): void {
    this.editId.set(c.id);
    this.form.setValue({ code: c.code, libelle: c.libelle, type: c.type });
    this.error.set('');
    this.showModal.set(true);
  }

  closeModal(): void {
    this.showModal.set(false);
  }

  submit(): void {
    if (this.form.invalid) return;
    this.submitting.set(true);
    this.error.set('');

    const payload = this.form.value as { code: string; libelle: string; type: TypeCompte };
    const id = this.editId();

    const obs = id
      ? this.api.updateCompte(id, payload)
      : this.api.createCompte(payload);

    obs.subscribe({
      next: () => {
        this.load();
        this.showModal.set(false);
        this.submitting.set(false);
      },
      error: (err) => {
        this.error.set(err.error?.detail ?? 'Une erreur est survenue');
        this.submitting.set(false);
      },
    });
  }

  toggleActive(c: CompteAnalytique): void {
    this.api.updateCompte(c.id, { is_active: !c.is_active }).subscribe(() => this.load());
  }

  typeBadgeClass(type: TypeCompte): string {
    return { CHARGE: 'badge--danger', PRODUIT: 'badge--success', NEUTRE: 'badge--neutral' }[type];
  }

  typeLabel(type: TypeCompte): string {
    return { CHARGE: 'Charge', PRODUIT: 'Produit', NEUTRE: 'Neutre' }[type];
  }
}
