import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';

import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-login',
  imports: [CommonModule, ReactiveFormsModule],
  template: `
    <div class="login-box">
      <h1>Sign in</h1>
      <div class="error-banner" *ngIf="error">{{ error }}</div>
      <form [formGroup]="form" (ngSubmit)="submit()">
        <div class="form-field">
          <label for="username">Username</label>
          <input id="username" type="text" [formControl]="form.controls.username" autocomplete="username" />
        </div>
        <div class="form-field">
          <label for="password">Password</label>
          <input id="password" type="password" [formControl]="form.controls.password" autocomplete="current-password" />
        </div>
        <button type="submit" [disabled]="isSubmitting">Sign in</button>
      </form>
    </div>
  `,
})
export class LoginComponent {
  private readonly fb = inject(FormBuilder);
  private readonly auth = inject(AuthService);
  private readonly router = inject(Router);

  form = this.fb.group({
    username: ['', Validators.required],
    password: ['', Validators.required],
  });
  error: string | null = null;
  isSubmitting = false;

  submit(): void {
    if (this.form.invalid) {
      this.error = 'Username and password are required';
      return;
    }
    this.isSubmitting = true;
    this.error = null;
    this.auth.login(this.form.value.username!, this.form.value.password!).subscribe({
      next: () => this.router.navigate(['/dashboard']),
      error: (err: any) => {
        this.isSubmitting = false;
        const code = err?.error?.error?.code;
        if (code === 'INVALID_CREDENTIALS') {
          this.error = 'Invalid username or password';
        } else if (code === 'MISSING_FIELDS') {
          this.error = 'Username and password are required';
        } else {
          this.error = 'Sign-in failed';
        }
      },
    });
  }
}
