"""Registro de tutores, estudiantes y disponibilidad (RF-01..RF-03)."""
import re
import sqlite3

from .errors import ConflictError, NotFoundError, ValidationError

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
TIME_RE = re.compile(r"^([01]\d|2[0-3]):[0-5]\d$")


def _need(value, field):
    if not isinstance(value, str) or not value.strip():
        raise ValidationError("VALIDATION", f"El campo '{field}' es obligatorio.")
    return value.strip()


def create_tutor(db, name, subject):
    name, subject = _need(name, "name"), _need(subject, "subject")
    with db.tx() as c:
        cur = c.execute("INSERT INTO tutors(name, subject) VALUES(?,?)", (name, subject))
    return {"id": cur.lastrowid, "name": name, "subject": subject}


def create_student(db, name, email):
    name, email = _need(name, "name"), _need(email, "email")
    if not EMAIL_RE.match(email):
        raise ValidationError("VALIDATION", "El correo electrónico no es válido.")
    try:
        with db.tx() as c:
            cur = c.execute("INSERT INTO students(name, email) VALUES(?,?)", (name, email.lower()))
    except sqlite3.IntegrityError:
        raise ConflictError("EMAIL_TAKEN", "Ya existe un estudiante con ese correo.")
    return {"id": cur.lastrowid, "name": name, "email": email.lower()}


def get_tutor(db, tutor_id):
    rows = db.query("SELECT * FROM tutors WHERE id=?", (tutor_id,))
    if not rows:
        raise NotFoundError("Tutor no encontrado.")
    return rows[0]


def get_student(db, student_id):
    rows = db.query("SELECT * FROM students WHERE id=?", (student_id,))
    if not rows:
        raise NotFoundError("Estudiante no encontrado.")
    return rows[0]


def add_availability(db, tutor_id, weekday, start_time, end_time):
    get_tutor(db, tutor_id)
    if not isinstance(weekday, int) or isinstance(weekday, bool) or not 0 <= weekday <= 6:
        raise ValidationError("VALIDATION", "weekday debe estar entre 0 (lunes) y 6 (domingo).")
    if not (isinstance(start_time, str) and TIME_RE.match(start_time)
            and isinstance(end_time, str) and TIME_RE.match(end_time)):
        raise ValidationError("VALIDATION", "Las horas deben tener formato HH:MM.")
    if start_time >= end_time:
        raise ValidationError("VALIDATION", "La hora de inicio debe ser anterior a la de fin.")
    with db.tx() as c:
        cur = c.execute(
            "INSERT INTO availability(tutor_id, weekday, start_time, end_time) VALUES(?,?,?,?)",
            (tutor_id, weekday, start_time, end_time))
    return {"id": cur.lastrowid, "tutor_id": tutor_id, "weekday": weekday,
            "start_time": start_time, "end_time": end_time}
