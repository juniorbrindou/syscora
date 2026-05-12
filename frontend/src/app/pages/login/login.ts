import { Component, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { ApiService } from '../../services/api.service';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class LoginPage {
  private fb = inject(FormBuilder);
  private api = inject(ApiService);
  private auth = inject(AuthService);
  private router = inject(Router);

  form = this.fb.group({
    email: ['admin@syscora.com', [Validators.required, Validators.email]],
    password: ['Admin@2024', Validators.required],
  });

  loading = signal(false);
  error = signal('');

  submit(): void {
    if (this.form.invalid) return;
    this.loading.set(true);
    this.error.set('');

    const { email, password } = this.form.value;
    this.api.login(email!, password!).subscribe({
      next: (token) => {
        this.auth.saveSession(token);
        this.router.navigate(['/dashboard']);
      },
      error: (err) => {
        this.error.set(err.error?.detail ?? 'Erreur de connexion. Vérifiez vos identifiants.');
        this.loading.set(false);
      },
    });
  }
}
