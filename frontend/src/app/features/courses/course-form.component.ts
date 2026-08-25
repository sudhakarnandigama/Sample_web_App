import { CommonModule } from '@angular/common';
import { Component, inject, OnInit } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';

import { CourseService } from '../../core/services/course.service';

@Component({
  selector: 'app-course-form',
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  template: `
    <h1>{{ isEdit ? 'Edit Course' : 'New Course' }}</h1>
    <div class="card">
      <div class="error-banner" *ngIf="serverError">{{ serverError }}</div>
      <form [formGroup]="form" (ngSubmit)="submit()">
        <div class="form-field">
          <label for="title">Title</label>
          <input id="title" type="text" [formControl]="form.controls.title" />
          <div class="inline-error" *ngIf="titleError">{{ titleError }}</div>
        </div>
        <div class="form-field">
          <label for="description">Description</label>
          <textarea id="description" [formControl]="form.controls.description"></textarea>
          <div class="inline-error" *ngIf="descriptionError">{{ descriptionError }}</div>
        </div>
        <div class="form-field">
          <label for="duration_hours">Duration (hours)</label>
          <input id="duration_hours" type="number" [formControl]="form.controls.duration_hours" />
          <div class="inline-error" *ngIf="durationError">{{ durationError }}</div>
        </div>
        <div class="auth-actions">
          <button type="submit" [disabled]="isSubmitting">Save</button>
          <a class="btn secondary" routerLink="/courses">Cancel</a>
        </div>
      </form>
    </div>
  `,
})
export class CourseFormComponent implements OnInit {
  private readonly fb = inject(FormBuilder);
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly service = inject(CourseService);

  form = this.fb.group({
    title: ['', Validators.required],
    description: ['', Validators.required],
    duration_hours: [null as number | null, [Validators.required, Validators.min(1)]],
  });
  isEdit = false;
  isSubmitting = false;
  serverError: string | null = null;

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    this.isEdit = !!id;
    if (id) {
      this.service.get(Number(id)).subscribe({
        next: (course) =>
          this.form.patchValue({
            title: course.title,
            description: course.description,
            duration_hours: course.duration_hours,
          }),
        error: () => this.router.navigate(['/courses']),
      });
    }
  }

  get titleError(): string | null {
    return this.form.controls.title.touched && this.form.controls.title.invalid
      ? 'Title - Required'
      : null;
  }

  get descriptionError(): string | null {
    return this.form.controls.description.touched && this.form.controls.description.invalid
      ? 'Description - Required'
      : null;
  }

  get durationError(): string | null {
    const c = this.form.controls.duration_hours;
    if (!c.touched || !c.invalid) {
      return null;
    }
    return c.errors?.['min'] ? 'Duration must be greater than zero' : 'Duration - Required';
  }

  submit(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }
    this.isSubmitting = true;
    this.serverError = null;
    const payload = {
      title: this.form.value.title!,
      description: this.form.value.description!,
      duration_hours: this.form.value.duration_hours!,
    };
    const id = this.route.snapshot.paramMap.get('id');
    const request = id
      ? this.service.update(Number(id), payload)
      : this.service.create(payload);
    request.subscribe({
      next: () => this.router.navigate(['/courses']),
      error: (err) => {
        this.isSubmitting = false;
        this.serverError =
          err?.error?.error?.code === 'INVALID_COURSE' ? 'Invalid course data' : 'Save failed';
      },
    });
  }
}
