import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface AdminSummary {
  total_learners: number;
  total_courses: number;
  active_courses: number;
  completed_courses: number;
  certificates: number;
}

export interface LearnerSummary {
  assigned_courses: number;
  in_progress: number;
  completed: number;
  certificates: number;
}

@Injectable({ providedIn: 'root' })
export class DashboardService {
  constructor(private http: HttpClient) {}

  getSummary(): Observable<AdminSummary | LearnerSummary> {
    return this.http.get<AdminSummary | LearnerSummary>(`${environment.apiUrl}/dashboard`);
  }
}
