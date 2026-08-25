import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface Question {
  id: number;
  question_text: string;
  option_a: string;
  option_b: string;
  option_c: string;
  option_d: string;
}

export interface Assessment {
  id: number;
  course_id: number;
  title: string;
  passing_score: number;
  questions: Question[];
}

export interface SubmitResult {
  score: number;
  result: string;
}

export interface LastResult {
  score: number;
  result: string;
  courseId: number;
}

@Injectable({ providedIn: 'root' })
export class AssessmentService {
  lastResult: LastResult | null = null;

  constructor(private http: HttpClient) {}

  getAssessment(courseId: number): Observable<Assessment> {
    return this.http.get<Assessment>(`${environment.apiUrl}/assessments/${courseId}`);
  }

  submit(assessmentId: number, answers: Record<number, string>): Observable<SubmitResult> {
    return this.http.post<SubmitResult>(`${environment.apiUrl}/assessments/${assessmentId}/submit`, {
      answers,
    });
  }
}
