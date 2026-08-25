import { CommonModule } from '@angular/common';
import { Component, inject, OnInit } from '@angular/core';
import { forkJoin } from 'rxjs';

import { Assignment, AssignmentService } from '../../core/services/assignment.service';
import { AssessmentService, Attempt } from '../../core/services/assessment.service';
import { Course, CourseService } from '../../core/services/course.service';
import { Learner, LearnerService } from '../../core/services/learner.service';

interface LearnerReportRow {
  learner: string;
  course: string;
  progress: number;
  score: number | null;
  status: string;
}

interface CourseReportRow {
  course: string;
  total_learners: number;
  completed: number;
  in_progress: number;
  not_started: number;
}

@Component({
  selector: 'app-reports',
  imports: [CommonModule],
  template: `
    <h1>Reports</h1>

    <h2>Learner Report</h2>
    <table class="data-table">
      <thead>
        <tr>
          <th>Learner</th>
          <th>Course</th>
          <th>Progress</th>
          <th>Assessment Score</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr *ngFor="let row of learnerReport">
          <td>{{ row.learner }}</td>
          <td>{{ row.course }}</td>
          <td>{{ row.progress }}%</td>
          <td>{{ row.score === null ? '-' : row.score }}</td>
          <td><span class="badge" [ngClass]="row.status">{{ row.status }}</span></td>
        </tr>
      </tbody>
    </table>

    <h2>Course Report</h2>
    <table class="data-table">
      <thead>
        <tr>
          <th>Course</th>
          <th>Total Learners</th>
          <th>Completed</th>
          <th>In Progress</th>
          <th>Not Started</th>
        </tr>
      </thead>
      <tbody>
        <tr *ngFor="let row of courseReport">
          <td>{{ row.course }}</td>
          <td>{{ row.total_learners }}</td>
          <td>{{ row.completed }}</td>
          <td>{{ row.in_progress }}</td>
          <td>{{ row.not_started }}</td>
        </tr>
      </tbody>
    </table>
  `,
})
export class ReportsComponent implements OnInit {
  private readonly learnerService = inject(LearnerService);
  private readonly courseService = inject(CourseService);
  private readonly assignmentService = inject(AssignmentService);
  private readonly assessmentService = inject(AssessmentService);

  learnerReport: LearnerReportRow[] = [];
  courseReport: CourseReportRow[] = [];

  ngOnInit(): void {
    forkJoin([
      this.learnerService.list(),
      this.courseService.list(),
      this.assignmentService.list(),
      this.assessmentService.listAttempts(),
    ]).subscribe(([learners, courses, assignments, attempts]) => {
      this.learnerReport = this.buildLearnerReport(learners, courses, assignments, attempts);
      this.courseReport = this.buildCourseReport(courses, assignments);
    });
  }

  buildLearnerReport(
    learners: Learner[],
    courses: Course[],
    assignments: Assignment[],
    attempts: Attempt[]
  ): LearnerReportRow[] {
    const learnerNames = new Map(learners.map((l) => [l.id, l.name]));
    const courseTitles = new Map(courses.map((c) => [c.id, c.title]));
    return assignments.map((a) => {
      const pairAttempts = attempts
        .filter((t) => t.learner_id === a.learner_id && t.course_id === a.course_id)
        .sort((x, y) => y.id - x.id);
      const latest = pairAttempts[0];
      return {
        learner: a.learner_name ?? learnerNames.get(a.learner_id) ?? String(a.learner_id),
        course: a.course_title ?? courseTitles.get(a.course_id) ?? String(a.course_id),
        progress: a.progress,
        score: latest ? latest.score : null,
        status: a.status,
      };
    });
  }

  buildCourseReport(courses: Course[], assignments: Assignment[]): CourseReportRow[] {
    return courses.map((course) => {
      const rows = assignments.filter((a) => a.course_id === course.id);
      const learnerIds = new Set(rows.map((r) => r.learner_id));
      return {
        course: course.title,
        total_learners: learnerIds.size,
        completed: rows.filter((r) => r.status === 'COMPLETED').length,
        in_progress: rows.filter((r) => r.status === 'IN_PROGRESS').length,
        not_started: rows.filter((r) => r.status === 'NOT_STARTED').length,
      };
    });
  }
}
