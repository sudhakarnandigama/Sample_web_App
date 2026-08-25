import { CommonModule } from '@angular/common';
import { Component, inject, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';

import { Assessment, AssessmentService } from '../../core/services/assessment.service';

@Component({
  selector: 'app-assessment',
  imports: [CommonModule, FormsModule],
  template: `
    <div class="error-banner" *ngIf="notFound">No assessment for this course</div>

    <ng-container *ngIf="assessment">
      <h1>{{ assessment.title }}</h1>
      <div class="error-banner" *ngIf="answerError">{{ answerError }}</div>

      <div class="card" *ngFor="let question of assessment.questions">
        <h3>{{ question.question_text }}</h3>
        <div *ngFor="let option of options(question)">
          <label class="option-row">
            <input
              type="radio"
              [name]="'q' + question.id"
              [value]="option.key"
              (change)="choose(question.id, option.key)"
            />
            {{ option.key }}) {{ option.text }}
          </label>
        </div>
      </div>

      <button (click)="submit()" [disabled]="isSubmitting">Submit</button>
    </ng-container>
  `,
  styles: `
    .option-row {
      display: block;
      margin: 0.4rem 0;
      font-size: 1rem;
    }
  `,
})
export class AssessmentComponent implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly service = inject(AssessmentService);

  assessment: Assessment | null = null;
  answers: Record<number, string> = {};
  notFound = false;
  answerError: string | null = null;
  isSubmitting = false;

  ngOnInit(): void {
    const courseId = Number(this.route.snapshot.paramMap.get('courseId'));
    this.service.getAssessment(courseId).subscribe({
      next: (assessment) => (this.assessment = assessment),
      error: () => (this.notFound = true),
    });
  }

  options(question: any): { key: string; text: string }[] {
    return [
      { key: 'A', text: question.option_a },
      { key: 'B', text: question.option_b },
      { key: 'C', text: question.option_c },
      { key: 'D', text: question.option_d },
    ];
  }

  choose(questionId: number, option: string): void {
    this.answers[questionId] = option;
    this.answerError = null;
  }

  submit(): void {
    if (!this.assessment) {
      return;
    }
    const unanswered = this.assessment.questions.some((q) => !this.answers[q.id]);
    if (unanswered) {
      this.answerError = 'Please answer all questions';
      return;
    }
    this.isSubmitting = true;
    this.answerError = null;
    this.service.submit(this.assessment.id, this.answers).subscribe({
      next: (res) => {
        this.service.lastResult = {
          score: res.score,
          result: res.result,
          courseId: this.assessment!.course_id,
        };
        this.router.navigate(['/assessment/result']);
      },
      error: () => {
        this.isSubmitting = false;
        this.answerError = 'Submission failed';
      },
    });
  }
}
