import { Component, OnInit, inject } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { User } from '../models';

@Component({
  selector: 'app-shell',
  standalone: true,
  imports: [RouterOutlet, RouterLink, RouterLinkActive],
  templateUrl: './shell.html',
  styleUrl: './shell.css',
})
export class Shell implements OnInit {
  private auth = inject(AuthService);
  user: User | null = null;

  ngOnInit(): void {
    this.user = this.auth.user();
  }

  logout(): void {
    this.auth.logout();
  }

  get userInitials(): string {
    if (!this.user?.full_name) return '?';
    return this.user.full_name
      .split(' ')
      .slice(0, 2)
      .map((n) => n[0])
      .join('')
      .toUpperCase();
  }
}
