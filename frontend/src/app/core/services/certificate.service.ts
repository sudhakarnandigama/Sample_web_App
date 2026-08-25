import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface Certificate {
  id: number;
  learner_id: number;
  course_id: number;
  certificate_number: string;
  issued_date: string;
  status: string;
  learner_name?: string;
  course_title?: string;
}

@Injectable({ providedIn: 'root' })
export class CertificateService {
  constructor(private http: HttpClient) {}

  list(): Observable<Certificate[]> {
    return this.http.get<Certificate[]>(`${environment.apiUrl}/certificates`);
  }

  get(id: number): Observable<Certificate> {
    return this.http.get<Certificate>(`${environment.apiUrl}/certificates/${id}`);
  }

  generate(courseId: number, learnerId?: number): Observable<Certificate> {
    const body: { course_id: number; learner_id?: number } = { course_id: courseId };
    if (learnerId != null) {
      body.learner_id = learnerId;
    }
    return this.http.post<Certificate>(`${environment.apiUrl}/certificates`, body);
  }
}
