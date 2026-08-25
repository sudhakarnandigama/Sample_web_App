import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface Course {
  id: number;
  title: string;
  description: string;
  duration_hours: number;
  status: string;
  created_at: string;
}

export interface CoursePayload {
  title: string;
  description: string;
  duration_hours: number;
}

@Injectable({ providedIn: 'root' })
export class CourseService {
  constructor(private http: HttpClient) {}

  list(): Observable<Course[]> {
    return this.http.get<Course[]>(`${environment.apiUrl}/courses`);
  }

  get(id: number): Observable<Course> {
    return this.http.get<Course>(`${environment.apiUrl}/courses/${id}`);
  }

  create(data: CoursePayload): Observable<Course> {
    return this.http.post<Course>(`${environment.apiUrl}/courses`, data);
  }

  update(id: number, data: Partial<CoursePayload> & { status?: string }): Observable<Course> {
    return this.http.put<Course>(`${environment.apiUrl}/courses/${id}`, data);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${environment.apiUrl}/courses/${id}`);
  }
}
