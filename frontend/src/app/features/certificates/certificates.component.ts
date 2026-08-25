import { CommonModule } from '@angular/common';
import { Component, inject, OnInit } from '@angular/core';

import { Certificate, CertificateService } from '../../core/services/certificate.service';

@Component({
  selector: 'app-certificates',
  imports: [CommonModule],
  template: `
    <h1>Certificates</h1>

    <table class="data-table">
      <thead>
        <tr>
          <th>Certificate Number</th>
          <th>Learner</th>
          <th>Course</th>
          <th>Issue Date</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr *ngFor="let certificate of certificates" (click)="open(certificate)" class="clickable">
          <td>{{ certificate.certificate_number }}</td>
          <td>{{ certificate.learner_name ?? certificate.learner_id }}</td>
          <td>{{ certificate.course_title ?? certificate.course_id }}</td>
          <td>{{ certificate.issued_date }}</td>
          <td><span class="badge" [ngClass]="certificate.status">{{ certificate.status }}</span></td>
        </tr>
      </tbody>
    </table>

    <div class="card" *ngIf="selected">
      <h2>Certificate details</h2>
      <p><strong>Number:</strong> {{ selected.certificate_number }}</p>
      <p><strong>Learner:</strong> {{ selected.learner_name }}</p>
      <p><strong>Course:</strong> {{ selected.course_title }}</p>
      <p><strong>Issued:</strong> {{ selected.issued_date }}</p>
      <p><strong>Status:</strong> <span class="badge" [ngClass]="selected.status">{{ selected.status }}</span></p>
    </div>
  `,
  styles: `
    .clickable {
      cursor: pointer;
    }
  `,
})
export class CertificatesComponent implements OnInit {
  private readonly service = inject(CertificateService);

  certificates: Certificate[] = [];
  selected: Certificate | null = null;

  ngOnInit(): void {
    this.service.list().subscribe((certificates) => (this.certificates = certificates));
  }

  open(certificate: Certificate): void {
    this.service.get(certificate.id).subscribe((detail) => (this.selected = detail));
  }
}
