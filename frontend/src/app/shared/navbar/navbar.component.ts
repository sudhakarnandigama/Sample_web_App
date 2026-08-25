import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { Router, RouterLink, RouterLinkActive } from '@angular/router';

import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-navbar',
  imports: [CommonModule, RouterLink, RouterLinkActive],
  template: `
    <nav class="navbar" *ngIf="auth.isAuthenticated()">
      <span class="brand">Training & Certification</span>
      <a routerLink="/dashboard" routerLinkActive="active">Dashboard</a>
      <a routerLink="/courses" routerLinkActive="active">Courses</a>
      <a routerLink="/learners" routerLinkActive="active" *ngIf="auth.getRole() === 'ADMIN'">Learners</a>
      <a routerLink="/assignments" routerLinkActive="active" *ngIf="auth.getRole() === 'ADMIN'">Assignments</a>
      <a routerLink="/certificates" routerLinkActive="active">Certificates</a>
      <a routerLink="/reports" routerLinkActive="active" *ngIf="auth.getRole() === 'ADMIN'">Reports</a>
      <span class="spacer"></span>
      <button (click)="logout()">Logout</button>
    </nav>
  `,
})
export class NavbarComponent {
  constructor(
    public auth: AuthService,
    private router: Router
  ) {}

  logout(): void {
    this.auth.logout();
    this.router.navigate(['/login']);
  }
}
