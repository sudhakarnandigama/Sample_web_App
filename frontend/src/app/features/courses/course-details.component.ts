import { CommonModule } from '@angular/common';
import { Component, inject, OnInit } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { AuthService } from '../../core/services/auth.service';
import { Course, CourseService } from '../../core/services/course.service';

@Component({
  selector: 'app-course-details',
  imports: [CommonModule, RouterLink],
  template: `
    <div class="error-banner" *ngIf="notFound">Course not found</div>
    <div class="card" *ngIf="course">
      <h1>{{ course.title }}</h1>
      <p>{{ course.description }}</p>
      <p><strong>Duration:</strong> {{ course.duration_hours }} hours</p>
      <p><strong>Status:</strong> <span class="badge" [ngClass]="course.status">{{ course.status }}</span></p>
      <p><strong>Created:</strong> {{ course.created_at }}</p>
      <div class="auth-actions">
        <a class="btn" routerLink="/courses">Back</a>
        <a
          class="btn"
          *ngIf="auth.getRole() === 'LEARNER'"
          [routerLink]="['/assessment', course.id]"
        >Take assessment</a>
      </div>
    </div>
  `,
})
export class CourseDetailsComponent implements OnInit {
  readonly auth = inject(AuthService);
  private readonly route = inject(ActivatedRoute);
  private readonly service = inject(CourseService);

  course: Course | null = null;
  notFound = false;

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.service.get(id).subscribe({
      next: (course) => (this.course = course),
      error: () => (this.notFound = true),
    });
  }
}
