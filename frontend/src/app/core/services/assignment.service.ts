import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface Assignment {
  id: number;
  course_id: number;
  learner_id: number;
  progress: number;
  status: string;
  assigned_date: string;
  learner_name?: string;
  course_title?: string;
}

@Injectable({ providedIn: 'root' })
export class AssignmentService {
  constructor(private http: HttpClient) {}

  list(): Observable<Assignment[]> {
    return this.http.get<Assignment[]>(`${environment.apiUrl}/assignments`);
  }

  create(learner_id: number, course_id: number): Observable<Assignment> {
    return this.http.post<Assignment>(`${environment.apiUrl}/assignments`, {
      learner_id,
      course_id,
    });
  }
}
