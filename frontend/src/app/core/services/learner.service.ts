import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface Learner {
  id: number;
  user_id: number | null;
  name: string;
  email: string;
  department: string;
  status: string;
  created_at: string;
}

export interface LearnerPayload {
  name: string;
  email: string;
  department: string;
}

@Injectable({ providedIn: 'root' })
export class LearnerService {
  constructor(private http: HttpClient) {}

  list(): Observable<Learner[]> {
    return this.http.get<Learner[]>(`${environment.apiUrl}/learners`);
  }

  get(id: number): Observable<Learner> {
    return this.http.get<Learner>(`${environment.apiUrl}/learners/${id}`);
  }

  create(data: LearnerPayload): Observable<Learner> {
    return this.http.post<Learner>(`${environment.apiUrl}/learners`, data);
  }

  update(id: number, data: Partial<LearnerPayload> & { status?: string }): Observable<Learner> {
    return this.http.put<Learner>(`${environment.apiUrl}/learners/${id}`, data);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${environment.apiUrl}/learners/${id}`);
  }
}
