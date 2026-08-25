import { Routes } from '@angular/router';

import { authGuard, roleGuard } from './core/guards/auth.guard';
import { LoginComponent } from './features/login/login.component';
import { DashboardComponent } from './features/dashboard/dashboard.component';
import { CoursesComponent } from './features/courses/courses.component';
import { CourseDetailsComponent } from './features/courses/course-details.component';
import { CourseFormComponent } from './features/courses/course-form.component';

export const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'dashboard', component: DashboardComponent, canActivate: [authGuard] },
  { path: 'courses', component: CoursesComponent, canActivate: [authGuard] },
  { path: 'courses/new', component: CourseFormComponent, canActivate: [authGuard, roleGuard(['ADMIN'])] },
  { path: 'courses/:id/edit', component: CourseFormComponent, canActivate: [authGuard, roleGuard(['ADMIN'])] },
  { path: 'courses/:id', component: CourseDetailsComponent, canActivate: [authGuard] },
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  { path: '**', redirectTo: '/dashboard' },
];
