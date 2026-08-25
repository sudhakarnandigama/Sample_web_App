import { CommonModule } from '@angular/common';
import { Component, inject, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { AuthService } from '../../core/services/auth.service';
import { DashboardService } from '../../core/services/dashboard.service';

interface StatCard {
  label: string;
  value: number;
}

@Component({
  selector: 'app-dashboard',
  imports: [CommonModule],
  template: `
    <h1>Dashboard</h1>
    <div class="error-banner" *ngIf="error">{{ error }}</div>
    <div class="stats-grid" *ngIf="cards.length">
      <div class="stat-card" *ngFor="let card of cards">
        <div class="value">{{ card.value }}</div>
        <div class="label">{{ card.label }}</div>
      </div>
    </div>
  `,
})
export class DashboardComponent implements OnInit {
  private readonly auth = inject(AuthService);
  private readonly router = inject(Router);
  private readonly dashboard = inject(DashboardService);

  stats: any = null;
  error: string | null = null;

  ngOnInit(): void {
    this.dashboard.getSummary().subscribe({
      next: (stats) => (this.stats = stats),
      error: () => this.router.navigate(['/login']),
    });
  }

  get cards(): StatCard[] {
    if (!this.stats) {
      return [];
    }
    if (this.auth.getRole() === 'ADMIN') {
      return [
        { label: 'Total Learners', value: this.stats.total_learners },
        { label: 'Total Courses', value: this.stats.total_courses },
        { label: 'Active Courses', value: this.stats.active_courses },
        { label: 'Completed Courses', value: this.stats.completed_courses },
        { label: 'Certificates', value: this.stats.certificates },
      ];
    }
    return [
      { label: 'Assigned Courses', value: this.stats.assigned_courses },
      { label: 'In Progress', value: this.stats.in_progress },
      { label: 'Completed', value: this.stats.completed },
      { label: 'Certificates', value: this.stats.certificates },
    ];
  }
}
