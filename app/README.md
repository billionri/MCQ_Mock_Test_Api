# 📝 MCQ Mock Test API

A FastAPI-based backend for managing Multiple Choice Question (MCQ) mock tests.  
The system supports users, tests, sections, questions, attempts, answers, bookmarks, announcements, and feedback.

---

## 🚀 Features

- **User Management** – create and manage platform users.
- **Test Management** – create tests with multiple sections.
- **Question Bank** – store MCQ questions with options, correct answers, explanations, and difficulty.
- **Test Attempts** – record when users start and finish a test, along with their scores.
- **Answer Tracking** – store answers selected during an attempt.
- **Bookmarks** – allow users to save questions for later review.
- **Announcements** – share platform updates and news with all users.
- **Feedback** – collect feedback messages from users.

---

## 🗄 Database Structure & Relationships

- **users**
  - Linked to `test_attempts` via `user_id`
  - Linked to `bookmarks` via `user_id`
  - Linked to `feedback` via `user_id`

- **tests**
  - Linked to `sections` via `test_id`
  - Linked to `test_attempts` via `test_id`

- **sections**
  - Linked to `questions` via `section_id`

- **questions**
  - Linked to `sections` via `section_id`
  - Linked to `attempted_questions` via `question_id`
  - Linked to `bookmarks` via `question_id`

- **test_attempts**
  - Linked to `users` via `user_id`
  - Linked to `tests` via `test_id`
  - Linked to `attempted_questions` via `attempt_id`

- **attempted_questions**
  - Linked to `test_attempts` via `attempt_id`
  - Linked to `questions` via `question_id`

- **bookmarks**
  - Linked to `users` via `user_id`
  - Linked to `questions` via `question_id`

- **announcements**
  - Not directly linked to other tables

- **feedback**
  - Linked to `users` via `user_id`

---

## 📦 Installation

### 1️⃣ Clone the repository
```bash
git clone <your-repo-url>
cd MCQ_Mock_Test_Api
```
---
 
### 2️⃣ Install dependencies
```bash
pip install fastapi uvicorn 
```

### 3️⃣ Run the API
```bash
uvicorn app.main:app --reload 
```

Users

GET /users – list all users

POST /users – create a new user

Tests

GET /tests – list all tests

POST /tests – create a new test

Sections

GET /sections – list all sections

POST /sections – create a new section

Questions

GET /questions – list all questions

POST /questions – create a new question

Test Attempts

GET /test_attempts – list all attempts

POST /test_attempts – create a new attempt

Attempted Questions

GET /attempted_questions – list all attempted questions

POST /attempted_questions – create a new attempted question record

Bookmarks

GET /bookmarks – list all bookmarks

POST /bookmarks – create a new bookmark

Announcements

GET /announcements – list all announcements

POST /announcements – create a new announcement

Feedback

GET /feedback – list all feedback messages

POST /feedback – create new feedback