import { CommonModule } from '@angular/common';
import { Component, inject, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { AssessmentService } from '../../core/services/assessment.service';
import { CertificateService } from '../../core/services/certificate.service';

@Component({
  selector: 'app-assessment-result',
  imports: [CommonModule],
  template: `
    <div class="card">
      <h1>Assessment Result</h1>
      <p class="value">{{ score !== null ? score : '-' }} / 100</p>
      <p>
        <span class="badge" [ngClass]="result">{{ result }}</span>
      </p>
      <div class="error-banner" *ngIf="certError">{{ certError }}</div>
      <div class="auth-actions">
        <button *ngIf="result === 'PASS'" (click)="generate()" [disabled]="generating">
          Generate certificate
        </button>
        <a class="btn secondary" routerLink="/courses">Back to courses</a>
      </div>
    </div>
  `,
})
export class AssessmentResultComponent implements OnInit {
  private readonly router = inject(Router);
  private readonly assessments = inject(AssessmentService);
  private readonly certificates = inject(CertificateService);

  score: number | null = null;
  result: string | null = null;
  courseId: number | null = null;
  certError: string | null = null;
  generating = false;

  ngOnInit(): void {
    const last = this.assessments.lastResult;
    if (!last) {
      this.router.navigate(['/courses']);
      return;
    }
    this.score = last.score;
    this.result = last.result;
    this.courseId = last.courseId;
  }

  generate(): void {
    if (this.courseId === null) {
      return;
    }
    this.generating = true;
    this.certError = null;
    this.certificates.generate(this.courseId).subscribe({
      next: () => this.router.navigate(['/certificates']),
      error: (err) => {
        this.generating = false;
        const code = err?.error?.error?.code;
        if (code === 'NOT_ELIGIBLE') {
          this.certError = 'Complete the course first';
        } else if (code === 'CERTIFICATE_EXISTS') {
          this.certError = 'Certificate already generated';
        } else {
          this.certError = 'Certificate generation failed';
        }
      },
    });
  }
}
