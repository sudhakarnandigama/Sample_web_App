import { CommonModule } from '@angular/common';
import { Component, inject, OnInit } from '@angular/core';
import { AbstractControl, FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';

import { LearnerService } from '../../core/services/learner.service';

function emailFormat(control: AbstractControl) {
  if (!control.value) {
    return null;
  }
  return /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(control.value) ? null : { email: true };
}

@Component({
  selector: 'app-learner-form',
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  template: `
    <h1>{{ isEdit ? 'Edit Learner' : 'New Learner' }}</h1>
    <div class="card">
      <div class="error-banner" *ngIf="serverError">{{ serverError }}</div>
      <form [formGroup]="form" (ngSubmit)="submit()">
        <div class="form-field">
          <label for="name">Name</label>
          <input id="name" type="text" [formControl]="form.controls.name" />
          <div class="inline-error" *ngIf="nameError">{{ nameError }}</div>
        </div>
        <div class="form-field">
          <label for="email">Email</label>
          <input id="email" type="text" [formControl]="form.controls.email" />
          <div class="inline-error" *ngIf="emailError">{{ emailError }}</div>
        </div>
        <div class="form-field">
          <label for="department">Department</label>
          <input id="department" type="text" [formControl]="form.controls.department" />
          <div class="inline-error" *ngIf="departmentError">{{ departmentError }}</div>
        </div>
        <div class="auth-actions">
          <button type="submit" [disabled]="isSubmitting">Save</button>
          <a class="btn secondary" routerLink="/learners">Cancel</a>
        </div>
      </form>
    </div>
  `,
})
export class LearnerFormComponent implements OnInit {
  private readonly fb = inject(FormBuilder);
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly service = inject(LearnerService);

  form = this.fb.group({
    name: ['', Validators.required],
    email: ['', [Validators.required, emailFormat]],
    department: ['', Validators.required],
  });
  isEdit = false;
  isSubmitting = false;
  serverError: string | null = null;

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    this.isEdit = !!id;
    if (id) {
      this.service.get(Number(id)).subscribe({
        next: (learner) =>
          this.form.patchValue({
            name: learner.name,
            email: learner.email,
            department: learner.department,
          }),
        error: () => this.router.navigate(['/learners']),
      });
    }
  }

  get nameError(): string | null {
    return this.form.controls.name.touched && this.form.controls.name.invalid
      ? 'Name - Required'
      : null;
  }

  get emailError(): string | null {
    const c = this.form.controls.email;
    if (!c.touched || !c.invalid) {
      return null;
    }
    return c.errors?.['required'] ? 'Email - Required' : 'Enter a valid email address';
  }

  get departmentError(): string | null {
    return this.form.controls.department.touched && this.form.controls.department.invalid
      ? 'Department - Required'
      : null;
  }

  submit(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }
    this.isSubmitting = true;
    this.serverError = null;
    const payload = {
      name: this.form.value.name!,
      email: this.form.value.email!,
      department: this.form.value.department!,
    };
    const id = this.route.snapshot.paramMap.get('id');
    const request = id
      ? this.service.update(Number(id), payload)
      : this.service.create(payload);
    request.subscribe({
      next: () => this.router.navigate(['/learners']),
      error: (err) => {
        this.isSubmitting = false;
        const code = err?.error?.error?.code;
        this.serverError =
          code === 'EMAIL_EXISTS'
            ? 'This email is already registered'
            : code === 'INVALID_LEARNER'
              ? 'Invalid learner data'
              : 'Save failed';
      },
    });
  }
}
