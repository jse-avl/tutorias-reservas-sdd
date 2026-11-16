"""Reservas y cancelaciones con las reglas BR-01..BR-10 (specs/business-rules.md)."""
from datetime import datetime, timedelta

from . import registry
from .errors import ConflictError, NotFoundError, ValidationError

FMT = "%Y-%m-%dT%H:%M"
DURATIONS = (30, 60)
MAX_ACTIVE_PER_WEEK = 3
CANCEL_MIN_HOURS = 2


def parse_dt(value, field="start"):
    try:
        return datetime.strptime(value, FMT)
    except (TypeError, ValueError):
        raise ValidationError("VALIDATION", f"'{field}' debe tener formato YYYY-MM-DDTHH:MM.")


def fmt(dt):
    return dt.strftime(FMT)


def has_overlap(conn, column, owner_id, start, end):
    """BR-09: intervalos semiabiertos [start, end). Solo cuentan reservas 'confirmed'."""
    row = conn.execute(
        f"SELECT 1 FROM bookings WHERE {column}=? AND status='confirmed' AND start < ? AND end > ? LIMIT 1",
        (owner_id, fmt(end), fmt(start))).fetchone()
    return row is not None


def within_availability(conn, tutor_id, start, end):
    if start.date() != end.date():
        return False
    row = conn.execute(
        "SELECT 1 FROM availability WHERE tutor_id=? AND weekday=? AND start_time<=? AND end_time>=? LIMIT 1",
        (tutor_id, start.weekday(), start.strftime("%H:%M"), end.strftime("%H:%M"))).fetchone()
    return row is not None


def create_booking(db, tutor_id, student_id, start, minutes, now):
    registry.get_tutor(db, tutor_id)
    registry.get_student(db, student_id)
    if minutes not in DURATIONS or isinstance(minutes, bool):
        raise ValidationError("INVALID_DURATION", "La duración debe ser de 30 o 60 minutos.")
    start_dt = parse_dt(start)
    if start_dt.minute % 30 != 0:
        raise ValidationError("INVALID_START", "La hora de inicio debe ser en punto o y media.")
    if start_dt <= now:
        raise ValidationError("PAST_DATE", "No se puede reservar en el pasado.")
    end_dt = start_dt + timedelta(minutes=minutes)

    with db.tx() as c:  # sección crítica: verificar + insertar es atómico
        if not within_availability(c, tutor_id, start_dt, end_dt):
            raise ValidationError("OUTSIDE_AVAILABILITY", "El horario está fuera de la disponibilidad del tutor.")
        if has_overlap(c, "tutor_id", tutor_id, start_dt, end_dt):
            raise ConflictError("TUTOR_CONFLICT", "El tutor ya tiene una reserva en ese horario.")
        if has_overlap(c, "student_id", student_id, start_dt, end_dt):
            raise ConflictError("STUDENT_CONFLICT", "Ya tienes otra tutoría en ese horario.")
        monday = (start_dt - timedelta(days=start_dt.weekday())).replace(hour=0, minute=0)
        count = c.execute(
            "SELECT COUNT(*) FROM bookings WHERE student_id=? AND status='confirmed' AND start>=? AND start<?",
            (student_id, fmt(monday), fmt(monday + timedelta(days=7)))).fetchone()[0]
        if count >= MAX_ACTIVE_PER_WEEK:
            raise ConflictError("WEEKLY_LIMIT",
                                f"Máximo {MAX_ACTIVE_PER_WEEK} tutorías por semana.")
        cur = c.execute(
            "INSERT INTO bookings(tutor_id, student_id, start, end, status, created_at) "
            "VALUES(?,?,?,?, 'confirmed', ?)",
            (tutor_id, student_id, fmt(start_dt), fmt(end_dt), fmt(now)))
    return get_booking(db, cur.lastrowid)


def get_booking(db, booking_id):
    rows = db.query("SELECT * FROM bookings WHERE id=?", (booking_id,))
    if not rows:
        raise NotFoundError("Reserva no encontrada.")
    return rows[0]


def cancel_booking(db, booking_id, now):
    with db.tx() as c:
        row = c.execute("SELECT * FROM bookings WHERE id=?", (booking_id,)).fetchone()
        if row is None:
            raise NotFoundError("Reserva no encontrada.")
        if row["status"] == "cancelled":
            raise ConflictError("ALREADY_CANCELLED", "La reserva ya estaba cancelada.")
        if parse_dt(row["start"]) - now < timedelta(hours=CANCEL_MIN_HOURS):
            raise ConflictError("TOO_LATE_TO_CANCEL",
                                f"Solo se puede cancelar con {CANCEL_MIN_HOURS} horas de anticipación.")
        c.execute("UPDATE bookings SET status='cancelled' WHERE id=?", (booking_id,))
    return get_booking(db, booking_id)


def list_bookings(db, student_id):
    registry.get_student(db, student_id)
    return db.query("SELECT * FROM bookings WHERE student_id=? ORDER BY start", (student_id,))
