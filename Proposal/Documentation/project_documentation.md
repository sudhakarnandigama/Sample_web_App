# Employee Training & Certification Demo System

## 1. Project Overview

The **Employee Training & Certification Demo System** is a simple demo-purpose web application.

It demonstrates a complete application using:

- **Frontend:** Angular
- **Backend:** Python + FastAPI
- **Database:** SQLite
- **API:** REST APIs
- **ORM:** SQLAlchemy

The application is intentionally simple. It is designed for demonstrations, UI/API testing, database testing, and coding-agent development.

> **Important:** This is a demo project only. Do not implement unnecessary enterprise-level complexity.

---

## 2. Project Objective

The application allows an administrator to manage training courses and learners.

Learners can:

- View assigned courses
- Track course progress
- Take assessments
- View their results
- Receive a certificate after successfully completing a course

The complete demo flow is:

```text
Admin Login
    ↓
Create Course
    ↓
Create Learner
    ↓
Assign Course
    ↓
Learner Login
    ↓
View Course
    ↓
Update Progress
    ↓
Take Assessment
    ↓
Pass Assessment
    ↓
Generate Certificate
```

---

# 3. Technology Stack

| Layer | Technology |
|---|---|
| Frontend | Angular |
| Backend | Python |
| Backend Framework | FastAPI |
| Database | SQLite |
| ORM | SQLAlchemy |
| API | REST / JSON |
| Authentication | Simple demo authentication |
| Development IDE | VS Code |

No separate database server is required because SQLite stores the database in a local file.

---

# 4. User Roles

## 4.1 Admin

The Admin can:

- Login
- View dashboard
- Create courses
- Edit courses
- Delete courses
- Create learners
- Edit learners
- Delete learners
- Assign courses
- View learner progress
- Manage assessments
- View certificates
- View basic reports

## 4.2 Learner

The Learner can:

- Login
- View dashboard
- View assigned courses
- View course details
- Update course progress
- Take assessments
- View assessment results
- View certificates

---

# 5. Application Modules

## 5.1 Login

Features:

- Username and password
- Admin login
- Learner login
- Role-based navigation
- Logout

For this demo, authentication should remain simple.

---

## 5.2 Dashboard

### Admin Dashboard

Display:

- Total Learners
- Total Courses
- Active Courses
- Completed Courses
- Certificates Issued

Example:

```text
-----------------------------------------
        Training Dashboard
-----------------------------------------

Total Learners       25
Total Courses        08
Active Courses       06
Completed Courses    15
Certificates Issued  10
-----------------------------------------
```

### Learner Dashboard

Display:

- Assigned Courses
- Courses In Progress
- Completed Courses
- Certificates

---

# 6. Course Management

Admin should be able to:

- Add course
- View courses
- Edit course
- Delete course
- Activate/deactivate course

### Course Fields

```text
Course ID
Course Title
Description
Duration
Status
Created Date
```

### Sample Courses

```text
1. Java Full Stack Development
2. Python Fundamentals
3. Web Development Basics
```

---

# 7. Learner Management

Admin should be able to:

- Add learner
- View learner
- Edit learner
- Delete learner
- Assign courses

### Learner Fields

```text
Learner ID
Name
Email
Department
Status
Created Date
```

### Sample Learners

```text
John Doe
Priya Sharma
Rahul Kumar
Anjali Rao
David Smith
```

---

# 8. Course Assignment

Admin can assign a course to a learner.

Example:

```text
Learner:
John Doe

Course:
Python Fundamentals

Progress:
Not Started
```

Possible progress states:

```text
Not Started
In Progress
Completed
```

---

# 9. Progress Tracking

Learners can update their course progress.

Example:

```text
Python Fundamentals

Progress: 65%

Status: In Progress
```

For simplicity, progress can be represented using:

- Percentage
- Status

---

# 10. Assessment

Each course can have a simple assessment.

The assessment should support multiple-choice questions.

### Example

```text
Question:

Which language is commonly used with FastAPI?

A. Python
B. Java
C. C#
D. PHP
```

The learner selects an answer and submits the assessment.

The system calculates:

```text
Total Questions: 10
Correct Answers: 8
Score: 80%
Result: PASS
```

---

# 11. Certification

If the learner:

1. Completes the course
2. Passes the assessment

the system creates a certificate record.

### Certificate Information

```text
Certificate Number
Learner Name
Course Name
Issue Date
Status
```

Example:

```text
Certificate Number: CERT-2026-001
Learner: John Doe
Course: Python Fundamentals
Issue Date: 14-Aug-2026
Status: Certified
```

For the demo, a simple certificate page is sufficient. A complex PDF-generation system is not required unless specifically needed.

---

# 12. Reports

Only basic reports are required.

### Learner Report

Display:

```text
Learner
Course
Progress
Assessment Score
Status
```

### Course Report

Display:

```text
Course
Total Learners
Completed
In Progress
Not Started
```

---

# 13. Angular Frontend Structure

Recommended structure:

```text
frontend/
├── src/
│   ├── app/
│   │   ├── core/
│   │   │   ├── services/
│   │   │   │   ├── auth.service.ts
│   │   │   │   ├── course.service.ts
│   │   │   │   ├── learner.service.ts
│   │   │   │   ├── assessment.service.ts
│   │   │   │   └── certificate.service.ts
│   │   │   ├── guards/
│   │   │   │   └── auth.guard.ts
│   │   │   └── interceptors/
│   │   │       └── auth.interceptor.ts
│   │   │
│   │   ├── shared/
│   │   │   ├── navbar/
│   │   │   ├── sidebar/
│   │   │   └── confirmation-dialog/
│   │   │
│   │   ├── features/
│   │   │   ├── login/
│   │   │   ├── dashboard/
│   │   │   ├── courses/
│   │   │   ├── learners/
│   │   │   ├── assignments/
│   │   │   ├── assessments/
│   │   │   └── certificates/
│   │   │
│   │   ├── app.routes.ts
│   │   └── app.config.ts
│   │
│   └── assets/
│
├── angular.json
├── package.json
└── tsconfig.json
```

---

# 14. Python Backend Structure

Use FastAPI for the backend.

```text
backend/
├── app/
│   ├── main.py
│   ├── database.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── course.py
│   │   ├── learner.py
│   │   ├── assignment.py
│   │   ├── assessment.py
│   │   └── certificate.py
│   │
│   ├── schemas/
│   │   ├── user.py
│   │   ├── course.py
│   │   ├── learner.py
│   │   ├── assessment.py
│   │   └── certificate.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── dashboard.py
│   │   ├── courses.py
│   │   ├── learners.py
│   │   ├── assignments.py
│   │   ├── assessments.py
│   │   └── certificates.py
│   │
│   └── services/
│       ├── auth_service.py
│       ├── assessment_service.py
│       └── certificate_service.py
│
├── requirements.txt
└── training_demo.db
```

---

# 15. SQLite Database

The SQLite database file can be:

```text
training_demo.db
```

No PostgreSQL, MySQL, or other database server is required.

---

# 16. Database Tables

## 16.1 users

```text
id
username
password
role
full_name
```

Example roles:

```text
ADMIN
LEARNER
```

---

## 16.2 courses

```text
id
title
description
duration
status
created_at
```

---

## 16.3 learners

```text
id
name
email
department
status
created_at
```

---

## 16.4 course_assignments

```text
id
course_id
learner_id
progress
status
assigned_date
```

---

## 16.5 assessments

```text
id
course_id
title
passing_score
```

---

## 16.6 questions

```text
id
assessment_id
question_text
option_a
option_b
option_c
option_d
correct_option
```

---

## 16.7 assessment_attempts

```text
id
assessment_id
learner_id
score
result
attempted_at
```

---

## 16.8 certificates

```text
id
learner_id
course_id
certificate_number
issued_date
status
```

---

# 17. Database Relationships

```text
users
  │
  └── learners

courses
  │
  ├── course_assignments
  │        │
  │        └── learners
  │
  └── assessments
           │
           └── questions

learners
  │
  ├── assessment_attempts
  │
  └── certificates
```

---

# 18. REST API

Base URL:

```text
http://localhost:8000/api
```

## Authentication

### Login

```http
POST /api/auth/login
```

Request:

```json
{
  "username": "admin",
  "password": "admin123"
}
```

---

# 19. Dashboard APIs

```http
GET /api/dashboard
```

Example response:

```json
{
  "total_learners": 5,
  "total_courses": 3,
  "completed_courses": 2,
  "certificates": 2
}
```

---

# 20. Course APIs

### Get Courses

```http
GET /api/courses
```

### Get Course

```http
GET /api/courses/{id}
```

### Create Course

```http
POST /api/courses
```

### Update Course

```http
PUT /api/courses/{id}
```

### Delete Course

```http
DELETE /api/courses/{id}
```

---

# 21. Learner APIs

### Get Learners

```http
GET /api/learners
```

### Get Learner

```http
GET /api/learners/{id}
```

### Create Learner

```http
POST /api/learners
```

### Update Learner

```http
PUT /api/learners/{id}
```

### Delete Learner

```http
DELETE /api/learners/{id}
```

---

# 22. Assignment APIs

### Assign Course

```http
POST /api/assignments
```

Example:

```json
{
  "learner_id": 1,
  "course_id": 2
}
```

### Update Progress

```http
PUT /api/assignments/{id}/progress
```

Example:

```json
{
  "progress": 75,
  "status": "IN_PROGRESS"
}
```

---

# 23. Assessment APIs

### Get Assessment

```http
GET /api/assessments/{course_id}
```

### Submit Assessment

```http
POST /api/assessments/{id}/submit
```

Example:

```json
{
  "learner_id": 1,
  "answers": {
    "1": "A",
    "2": "C",
    "3": "B"
  }
}
```

Example response:

```json
{
  "score": 80,
  "result": "PASS"
}
```

---

# 24. Certificate APIs

### Get Certificates

```http
GET /api/certificates
```

### Get Certificate

```http
GET /api/certificates/{id}
```

### Generate Certificate

```http
POST /api/certificates
```

---

# 25. Demo Login Accounts

## Admin

```text
Username: admin
Password: admin123
Role: ADMIN
```

## Learner

```text
Username: learner
Password: learner123
Role: LEARNER
```

These credentials are only for local demonstration.

---

# 26. Sample Demo Data

## Courses

```text
Java Full Stack Development
Python Fundamentals
Web Development Basics
```

## Learners

```text
John Doe
Priya Sharma
Rahul Kumar
Anjali Rao
David Smith
```

## Progress States

```text
Not Started
In Progress
Completed
```

## Assessment Results

```text
Passed
Failed
```

---

# 27. Backend Installation

## Step 1: Create Virtual Environment

```bash
cd backend

python -m venv venv
```

## Step 2: Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux/macOS

```bash
source venv/bin/activate
```

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 28. requirements.txt

The initial requirements can be:

```text
fastapi
uvicorn[standard]
sqlalchemy
pydantic
python-multipart
```

Additional packages should only be added when actually required.

---

# 29. Start Backend

Run:

```bash
uvicorn app.main:app --reload
```

Backend:

```text
http://localhost:8000
```

FastAPI Swagger documentation:

```text
http://localhost:8000/docs
```

---

# 30. Frontend Installation

Go to the Angular project:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start Angular:

```bash
ng serve
```

Frontend:

```text
http://localhost:4200
```

---

# 31. Angular API Configuration

Create an environment configuration containing:

```typescript
export const environment = {
  apiUrl: 'http://localhost:8000/api'
};
```

Angular services should use this URL when communicating with FastAPI.

Example:

```text
Angular
   ↓
HttpClient
   ↓
FastAPI REST API
   ↓
SQLAlchemy
   ↓
SQLite
```

---

# 32. CORS

FastAPI should allow the Angular development server to access the API.

For local development, allow:

```text
http://localhost:4200
```

Do not configure broad production CORS rules because this is a demo application.

---

# 33. Angular Pages

The application should contain these basic pages:

```text
Login
Dashboard
Courses
Course Details
Add Course
Edit Course
Learners
Add Learner
Edit Learner
Course Assignments
Assessment
Assessment Result
Certificates
Reports
```

---

# 34. Admin Navigation

Example:

```text
Dashboard
Courses
Learners
Assignments
Assessments
Certificates
Reports
Logout
```

---

# 35. Learner Navigation

Example:

```text
Dashboard
My Courses
Assessments
My Certificates
Logout
```

---

# 36. Recommended UI

The UI should be:

- Simple
- Clean
- Professional
- Responsive
- Easy to understand
- Suitable for a demo

Use standard:

- Tables
- Cards
- Forms
- Buttons
- Modals
- Progress bars
- Status badges

Avoid unnecessary animations and complicated UI components.

---

# 37. Complete Demo Workflow

## Step 1

Login as Admin.

```text
Username: admin
Password: admin123
```

## Step 2

Open Courses.

Create:

```text
Python Fundamentals
```

## Step 3

Create a learner:

```text
John Doe
john@example.com
IT
```

## Step 4

Assign:

```text
Python Fundamentals
        ↓
John Doe
```

## Step 5

Logout.

## Step 6

Login as Learner.

```text
Username: learner
Password: learner123
```

## Step 7

Open My Courses.

The learner should see:

```text
Python Fundamentals
Progress: 0%
Status: Not Started
```

## Step 8

Update progress:

```text
25%
50%
75%
100%
```

## Step 9

Take the assessment.

Example:

```text
Total Questions: 10
Correct Answers: 8
Score: 80%
Result: PASS
```

## Step 10

Generate/view the certificate.

```text
Certificate Number: CERT-2026-001
Learner: John Doe
Course: Python Fundamentals
Status: Certified
```

This completes the main demo.

---

# 38. Error Handling

The application should handle basic errors.

Examples:

```text
Invalid username/password
Course not found
Learner not found
Course already assigned
Assessment not found
Invalid assessment submission
Certificate already generated
```

Display simple user-friendly messages in Angular.

---

# 39. Validation

Basic frontend validation should be implemented.

Examples:

### Course

```text
Title - Required
Description - Required
Duration - Required
```

### Learner

```text
Name - Required
Email - Required
Department - Required
```

### Login

```text
Username - Required
Password - Required
```

---

# 40. Testing Checklist

## Authentication

- [ ] Admin can login
- [ ] Learner can login
- [ ] Invalid credentials show an error
- [ ] Logout works

## Courses

- [ ] Course list loads
- [ ] Course can be created
- [ ] Course can be edited
- [ ] Course can be deleted
- [ ] Course details can be viewed

## Learners

- [ ] Learner list loads
- [ ] Learner can be created
- [ ] Learner can be edited
- [ ] Learner can be deleted

## Assignments

- [ ] Course can be assigned
- [ ] Assigned course appears for learner
- [ ] Progress can be updated

## Assessment

- [ ] Questions load
- [ ] Answers can be selected
- [ ] Assessment can be submitted
- [ ] Score is calculated
- [ ] Pass/fail result is displayed

## Certification

- [ ] Certificate is created after passing
- [ ] Certificate appears in learner account
- [ ] Certificate information is displayed correctly

---

# 41. Development Order

Implement the project in this order:

1. Create Angular project.
2. Create FastAPI project.
3. Configure SQLite.
4. Configure SQLAlchemy.
5. Create database models.
6. Add sample database data.
7. Implement login API.
8. Create Angular login page.
9. Implement dashboard API.
10. Create dashboard UI.
11. Implement course CRUD.
12. Create course UI.
13. Implement learner CRUD.
14. Create learner UI.
15. Implement course assignment.
16. Implement progress tracking.
17. Implement assessment.
18. Implement assessment result.
19. Implement certificate functionality.
20. Create basic reports.
21. Test the complete workflow.
22. Fix UI/API issues.

---

# 42. Project Scope Restrictions

Because this is a **demo project**, do NOT add unnecessary complexity.

Do not implement:

- Microservices
- Kubernetes
- Redis
- Message queues
- Complex event-driven architecture
- Multiple databases
- Advanced cloud infrastructure
- Complex OAuth providers
- Payment systems
- Email notification systems
- Advanced analytics
- AI features
- Complex certificate verification
- Enterprise-level permission management

The goal is to have a small, clean, working application.

---

# 43. Suggested Root Project Structure

```text
employee-training-demo/
│
├── frontend/
│   └── Angular application
│
├── backend/
│   ├── app/
│   ├── requirements.txt
│   └── training_demo.db
│
├── README.md
└── .gitignore
```

---

# 44. .gitignore

Recommended entries:

```text
# Angular
node_modules/
dist/

# Python
venv/
__pycache__/
*.pyc

# SQLite
*.db

# Environment
.env

# IDE
.vscode/
.idea/
```

---

# 45. Final Demo Objective

The final application should demonstrate this complete scenario:

```text
Admin
  ↓
Login
  ↓
Create Course
  ↓
Create Learner
  ↓
Assign Course
  ↓
Logout
  ↓
Learner Login
  ↓
View Assigned Course
  ↓
Complete Course
  ↓
Take Assessment
  ↓
Pass Assessment
  ↓
Certificate Generated
  ↓
View Certificate
```

The project should remain **simple, functional, and easy to understand**. The primary purpose is to demonstrate an end-to-end Angular + Python + SQLite application and provide a realistic sample project for development and coding-agent testing.
