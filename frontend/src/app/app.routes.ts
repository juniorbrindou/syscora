import { Routes } from '@angular/router';
import { authGuard } from './guards/auth.guard';

export const routes: Routes = [
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  {
    path: 'login',
    loadComponent: () => import('./pages/login/login').then((m) => m.LoginPage),
  },
  {
    path: '',
    loadComponent: () => import('./layout/shell').then((m) => m.Shell),
    canActivate: [authGuard],
    children: [
      {
        path: 'dashboard',
        loadComponent: () => import('./pages/dashboard/dashboard').then((m) => m.DashboardPage),
      },
      {
        path: 'ecritures',
        loadComponent: () => import('./pages/ecritures/ecritures').then((m) => m.EcrituresPage),
      },
      {
        path: 'comptes',
        loadComponent: () => import('./pages/comptes/comptes').then((m) => m.ComptesPage),
      },
      {
        path: 'axes',
        loadComponent: () => import('./pages/axes/axes').then((m) => m.AxesPage),
      },
    ],
  },
  { path: '**', redirectTo: '/dashboard' },
];
