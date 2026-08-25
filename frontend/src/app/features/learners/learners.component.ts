import { CommonModule } from '@angular/common';
import { Component, inject, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { Learner, LearnerService } from '../../core/services/learner.service';

@Component({
  selector: 'app-learners',
  imports: [CommonModule],
  template: `
    <div class="page-head">
      <h1>Learners</h1>
      <button (click)="router.navigate(['/learners/new'])">Add Learner</button>
    </div>

    <table class="data-table">
      <thead>
        <tr>
          <th>Name</th>
          <th>Email</th>
          <th>Department</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr *ngFor="let learner of learners">
          <td>{{ learner.name }}</td>
          <td>{{ learner.email }}</td>
          <td>{{ learner.department }}</td>
          <td><span class="badge" [ngClass]="learner.status">{{ learner.status }}</span></td>
          <td>
            <button class="small" (click)="router.navigate(['/learners', learner.id, 'edit'])">Edit</button>
            <button class="small danger" (click)="remove(learner)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
  `,
})
export class LearnersComponent implements OnInit {
  readonly router = inject(Router);
  private readonly service = inject(LearnerService);

  learners: Learner[] = [];

  ngOnInit(): void {
    this.load();
  }

  load(): void {
    this.service.list().subscribe((learners) => (this.learners = learners));
  }

  remove(learner: Learner): void {
    if (window.confirm(`Delete learner "${learner.name}"?`)) {
      this.service.delete(learner.id).subscribe(() => this.load());
    }
  }
}
