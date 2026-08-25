import { CommonModule } from '@angular/common';
import { Component, inject, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { Assignment, AssignmentService } from '../../core/services/assignment.service';
import { Course, CourseService } from '../../core/services/course.service';
import { Learner, LearnerService } from '../../core/services/learner.service';

@Component({
  selector: 'app-assignments',
  imports: [CommonModule, FormsModule],
  template: `
    <h1>Assignments</h1>

    <div class="card">
      <div class="success-banner" *ngIf="success">{{ success }}</div>
      <div class="error-banner" *ngIf="error">{{ error }}</div>
      <form (ngSubmit)="submit()">
        <div class="form-field">
          <label for="learner">Learner</label>
          <select id="learner" [(ngModel)]="learnerId" name="learner">
            <option [ngValue]="null">Select learner</option>
            <option *ngFor="let learner of learners" [ngValue]="learner.id">
              {{ learner.name }} ({{ learner.email }})
            </option>
          </select>
        </div>
        <div class="form-field">
          <label for="course">Course</label>
          <select id="course" [(ngModel)]="courseId" name="course">
            <option [ngValue]="null">Select course</option>
            <option *ngFor="let course of courses" [ngValue]="course.id">{{ course.title }}</option>
          </select>
        </div>
        <button type="submit" [disabled]="learnerId === null || courseId === null">Assign</button>
      </form>
    </div>

    <h2>Existing assignments</h2>
    <table class="data-table">
      <thead>
        <tr>
          <th>Learner</th>
          <th>Course</th>
          <th>Progress</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr *ngFor="let assignment of assignments">
          <td>{{ assignment.learner_name ?? assignment.learner_id }}</td>
          <td>{{ assignment.course_title ?? assignment.course_id }}</td>
          <td>{{ assignment.progress }}%</td>
          <td><span class="badge" [ngClass]="assignment.status">{{ assignment.status }}</span></td>
        </tr>
      </tbody>
    </table>
  `,
})
export class AssignmentsComponent implements OnInit {
  private readonly assignmentsService = inject(AssignmentService);
  private readonly learnerService = inject(LearnerService);
  private readonly courseService = inject(CourseService);

  learners: Learner[] = [];
  courses: Course[] = [];
  assignments: Assignment[] = [];
  learnerId: number | null = null;
  courseId: number | null = null;
  error: string | null = null;
  success: string | null = null;

  ngOnInit(): void {
    this.learnerService.list().subscribe((learners) => (this.learners = learners));
    this.courseService.list().subscribe((courses) => (this.courses = courses));
    this.loadAssignments();
  }

  loadAssignments(): void {
    this.assignmentsService.list().subscribe((assignments) => (this.assignments = assignments));
  }

  submit(): void {
    if (this.learnerId === null || this.courseId === null) {
      return;
    }
    this.error = null;
    this.success = null;
    this.assignmentsService.create(this.learnerId, this.courseId).subscribe({
      next: () => {
        this.success = 'Course assigned to learner';
        this.learnerId = null;
        this.courseId = null;
        this.loadAssignments();
      },
      error: (err) => {
        const code = err?.error?.error?.code;
        this.error =
          code === 'ASSIGNMENT_EXISTS'
            ? 'Course already assigned to this learner'
            : 'Assignment failed';
      },
    });
  }
}
