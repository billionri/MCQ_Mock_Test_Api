from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import sqlite3

DB_PATH = "mcq_mock_test_api_db"

app = FastAPI(title="MCQ Mock Test API - Full CRUD")

def get_conn():
    # Allow multithreaded access and wait for a lock up to 5s
    conn = sqlite3.connect(DB_PATH, timeout=5, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


# --------------------
# USERS
# --------------------
class User(BaseModel):
    id: Optional[int]
    name: str
    email: str
    password_hash: str
    created_at: Optional[str]

@app.post("/users", response_model=User)
def add_user(user: User):
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (user.name, user.email, user.password_hash),
        )
        conn.commit()
        user.id = cur.lastrowid
        return user
    finally:
        conn.close()


@app.post("/users", response_model=User)
def add_user(user: User):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        (user.name, user.email, user.password_hash),
    )
    conn.commit()
    user.id = cur.lastrowid
    conn.close()
    return user

# --------------------
# TESTS
# --------------------
class Test(BaseModel):
    id: Optional[int]
    title: str
    description: Optional[str]
    total_marks: Optional[int] = 0
    duration_min: int
    created_at: Optional[str]

@app.get("/tests", response_model=List[Test])
def list_tests():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM tests").fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.post("/tests", response_model=Test)
def add_test(t: Test):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tests (title, description, total_marks, duration_min) VALUES (?, ?, ?, ?)",
        (t.title, t.description, t.total_marks, t.duration_min),
    )
    conn.commit()
    t.id = cur.lastrowid
    conn.close()
    return t

# --------------------
# SECTIONS
# --------------------
class Section(BaseModel):
    id: Optional[int]
    test_id: Optional[int]
    name: str
    order: Optional[int] = 1

@app.get("/sections", response_model=List[Section])
def list_sections():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM sections").fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.post("/sections", response_model=Section)
def add_section(s: Section):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO sections (test_id, name, order) VALUES (?, ?, ?)",
        (s.test_id, s.name, s.order),
    )
    conn.commit()
    s.id = cur.lastrowid
    conn.close()
    return s

# --------------------
# QUESTIONS
# --------------------
class Question(BaseModel):
    id: Optional[int]
    section_id: Optional[int]
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_option: Optional[str]
    explanation: Optional[str]
    difficulty: Optional[str]

@app.get("/questions", response_model=List[Question])
def list_questions():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM questions").fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.post("/questions", response_model=Question)
def add_question(q: Question):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO questions (section_id, question_text, option_a, option_b, option_c, option_d, correct_option, explanation, difficulty)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (q.section_id, q.question_text, q.option_a, q.option_b, q.option_c, q.option_d, q.correct_option, q.explanation, q.difficulty))
    conn.commit()
    q.id = cur.lastrowid
    conn.close()
    return q

# --------------------
# TEST ATTEMPTS
# --------------------
class TestAttempt(BaseModel):
    id: Optional[int]
    user_id: Optional[int]
    test_id: Optional[int]
    started_at: Optional[str]
    ended_at: Optional[str]
    score: Optional[int] = 0

@app.get("/test_attempts", response_model=List[TestAttempt])
def list_attempts():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM test_attempts").fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.post("/test_attempts", response_model=TestAttempt)
def add_attempt(a: TestAttempt):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO test_attempts (user_id, test_id, score) VALUES (?, ?, ?)",
        (a.user_id, a.test_id, a.score),
    )
    conn.commit()
    a.id = cur.lastrowid
    conn.close()
    return a

# --------------------
# ATTEMPTED QUESTIONS
# --------------------
class AttemptedQuestion(BaseModel):
    id: Optional[int]
    attempt_id: Optional[int]
    question_id: Optional[int]
    selected_option: Optional[str]
    is_correct: Optional[bool]

@app.get("/attempted_questions", response_model=List[AttemptedQuestion])
def list_attempted():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM attempted_questions").fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.post("/attempted_questions", response_model=AttemptedQuestion)
def add_attempted(aq: AttemptedQuestion):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO attempted_questions (attempt_id, question_id, selected_option, is_correct) VALUES (?, ?, ?, ?)",
        (aq.attempt_id, aq.question_id, aq.selected_option, aq.is_correct),
    )
    conn.commit()
    aq.id = cur.lastrowid
    conn.close()
    return aq

# --------------------
# BOOKMARKS
# --------------------
class Bookmark(BaseModel):
    id: Optional[int]
    user_id: Optional[int]
    question_id: Optional[int]
    created_at: Optional[str]

@app.get("/bookmarks", response_model=List[Bookmark])
def list_bookmarks():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM bookmarks").fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.post("/bookmarks", response_model=Bookmark)
def add_bookmark(b: Bookmark):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO bookmarks (user_id, question_id) VALUES (?, ?)",
        (b.user_id, b.question_id),
    )
    conn.commit()
    b.id = cur.lastrowid
    conn.close()
    return b

# --------------------
# ANNOUNCEMENTS
# --------------------
class Announcement(BaseModel):
    id: Optional[int]
    title: Optional[str]
    message: Optional[str]
    created_at: Optional[str]

@app.get("/announcements", response_model=List[Announcement])
def list_announcements():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM announcements").fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.post("/announcements", response_model=Announcement)
def add_announcement(a: Announcement):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO announcements (title, message) VALUES (?, ?)",
        (a.title, a.message),
    )
    conn.commit()
    a.id = cur.lastrowid
    conn.close()
    return a

# --------------------
# FEEDBACK
# --------------------
class Feedback(BaseModel):
    id: Optional[int]
    user_id: Optional[int]
    message: str
    created_at: Optional[str]

@app.get("/feedback", response_model=List[Feedback])
def list_feedback():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM feedback").fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.post("/feedback", response_model=Feedback)
def add_feedback(f: Feedback):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO feedback (user_id, message) VALUES (?, ?)",
        (f.user_id, f.message),
    )
    conn.commit()
    f.id = cur.lastrowid
    conn.close()
    return f
