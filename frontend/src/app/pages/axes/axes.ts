import { Component, OnInit, inject, signal } from '@angular/core';
import { NgClass } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { ApiService } from '../../services/api.service';
import { AxeAnalytique, TypeAxe } from '../../models';

@Component({
  selector: 'app-axes',
  standalone: true,
  imports: [ReactiveFormsModule, NgClass],
  templateUrl: './axes.html',
  styleUrl: './axes.css',
})
export class AxesPage implements OnInit {
  private api = inject(ApiService);
  private fb = inject(FormBuilder);

  axes = signal<AxeAnalytique[]>([]);
  showModal = signal(false);
  editId = signal<number | null>(null);
  submitting = signal(false);
  error = signal('');

  readonly typeOptions: { value: TypeAxe; label: string }[] = [
    { value: 'CENTRE_COUT', label: 'Centre de coût' },
    { value: 'PROJET', label: 'Projet' },
    { value: 'DEPARTEMENT', label: 'Département' },
  ];

  form = this.fb.group({
    code: ['', [Validators.required, Validators.maxLength(20)]],
    libelle: ['', [Validators.required, Validators.maxLength(200)]],
    type: ['CENTRE_COUT' as TypeAxe, Validators.required],
  });

  ngOnInit(): void {
    this.load();
  }

  load(): void {
    this.api.getAxes().subscribe((a) => this.axes.set(a));
  }

  openCreate(): void {
    this.editId.set(null);
    this.form.reset({ code: '', libelle: '', type: 'CENTRE_COUT' });
    this.error.set('');
    this.showModal.set(true);
  }

  openEdit(a: AxeAnalytique): void {
    this.editId.set(a.id);
    this.form.setValue({ code: a.code, libelle: a.libelle, type: a.type });
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

    const payload = this.form.value as { code: string; libelle: string; type: TypeAxe };
    const id = this.editId();

    const obs = id
      ? this.api.updateAxe(id, payload)
      : this.api.createAxe(payload);

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

  toggleActive(a: AxeAnalytique): void {
    this.api.updateAxe(a.id, { is_active: !a.is_active }).subscribe(() => this.load());
  }

  typeBadgeClass(type: TypeAxe): string {
    return { CENTRE_COUT: 'badge--primary', PROJET: 'badge--success', DEPARTEMENT: 'badge--warning' }[type];
  }

  typeLabel(type: TypeAxe): string {
    return { CENTRE_COUT: 'Centre de coût', PROJET: 'Projet', DEPARTEMENT: 'Département' }[type];
  }
}
