import { Routes } from '@angular/router';

import { authGuard, roleGuard } from './core/guards/auth.guard';
import { LoginComponent } from './features/login/login.component';
import { DashboardComponent } from './features/dashboard/dashboard.component';
import { CoursesComponent } from './features/courses/courses.component';
import { CourseDetailsComponent } from './features/courses/course-details.component';
import { CourseFormComponent } from './features/courses/course-form.component';
import { LearnersComponent } from './features/learners/learners.component';
import { LearnerFormComponent } from './features/learners/learner-form.component';
import { AssignmentsComponent } from './features/assignments/assignments.component';

export const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'dashboard', component: DashboardComponent, canActivate: [authGuard] },
  { path: 'courses', component: CoursesComponent, canActivate: [authGuard] },
  { path: 'courses/new', component: CourseFormComponent, canActivate: [authGuard, roleGuard(['ADMIN'])] },
  { path: 'courses/:id/edit', component: CourseFormComponent, canActivate: [authGuard, roleGuard(['ADMIN'])] },
  { path: 'courses/:id', component: CourseDetailsComponent, canActivate: [authGuard] },
  { path: 'learners', component: LearnersComponent, canActivate: [authGuard, roleGuard(['ADMIN'])] },
  { path: 'learners/new', component: LearnerFormComponent, canActivate: [authGuard, roleGuard(['ADMIN'])] },
  { path: 'learners/:id/edit', component: LearnerFormComponent, canActivate: [authGuard, roleGuard(['ADMIN'])] },
  { path: 'assignments', component: AssignmentsComponent, canActivate: [authGuard, roleGuard(['ADMIN'])] },
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  { path: '**', redirectTo: '/dashboard' },
];
