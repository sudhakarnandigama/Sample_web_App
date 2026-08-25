import { CommonModule } from '@angular/common';
import { Component, inject, OnInit } from '@angular/core';
import { Router, RouterLink } from '@angular/router';

import { AuthService } from '../../core/services/auth.service';
import { Course, CourseService } from '../../core/services/course.service';

@Component({
  selector: 'app-courses',
  imports: [CommonModule, RouterLink],
  template: `
    <div class="page-head">
      <h1>Courses</h1>
      <button *ngIf="isAdmin" (click)="router.navigate(['/courses/new'])">Add Course</button>
    </div>

    <table class="data-table">
      <thead>
        <tr>
          <th>Title</th>
          <th>Duration (hrs)</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr *ngFor="let course of courses">
          <td><a [routerLink]="['/courses', course.id]">{{ course.title }}</a></td>
          <td>{{ course.duration_hours }}</td>
          <td><span class="badge" [ngClass]="course.status">{{ course.status }}</span></td>
          <td *ngIf="isAdmin">
            <button class="small" (click)="router.navigate(['/courses', course.id, 'edit'])">Edit</button>
            <button class="small secondary" (click)="toggleStatus(course)">
              {{ course.status === 'ACTIVE' ? 'Deactivate' : 'Activate' }}
            </button>
            <button class="small danger" (click)="remove(course)">Delete</button>
          </td>
          <td *ngIf="!isAdmin">
            <a [routerLink]="['/courses', course.id]">View</a>
          </td>
        </tr>
      </tbody>
    </table>
  `,
})
export class CoursesComponent implements OnInit {
  readonly auth = inject(AuthService);
  readonly router = inject(Router);
  private readonly service = inject(CourseService);

  courses: Course[] = [];

  ngOnInit(): void {
    this.load();
  }

  get isAdmin(): boolean {
    return this.auth.getRole() === 'ADMIN';
  }

  load(): void {
    this.service.list().subscribe((courses) => (this.courses = courses));
  }

  toggleStatus(course: Course): void {
    const status = course.status === 'ACTIVE' ? 'INACTIVE' : 'ACTIVE';
    this.service.update(course.id, { status }).subscribe(() => this.load());
  }

  remove(course: Course): void {
    if (window.confirm(`Delete course "${course.title}"?`)) {
      this.service.delete(course.id).subscribe(() => this.load());
    }
  }
}
