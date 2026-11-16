"""Consulta de horarios libres (RF-04)."""
from datetime import datetime, timedelta

from . import registry
from .bookings import DURATIONS, TUTOR_BUFFER_MINUTES, has_overlap
from .errors import ValidationError


def free_slots(db, tutor_id, date, minutes, now):
    registry.get_tutor(db, tutor_id)
    if minutes not in DURATIONS:
        raise ValidationError("INVALID_DURATION", "La duración debe ser de 30 o 60 minutos.")
    try:
        day = datetime.strptime(date, "%Y-%m-%d")
    except (TypeError, ValueError):
        raise ValidationError("VALIDATION", "'date' debe tener formato YYYY-MM-DD.")
    windows = db.query(
        "SELECT start_time, end_time FROM availability WHERE tutor_id=? AND weekday=?",
        (tutor_id, day.weekday()))
    result = set()
    with db.tx() as c:
        for w in windows:
            h, m = map(int, w["start_time"].split(":"))
            cursor = day.replace(hour=h, minute=m)
            h, m = map(int, w["end_time"].split(":"))
            limit = day.replace(hour=h, minute=m)
            while cursor + timedelta(minutes=minutes) <= limit:
                end = cursor + timedelta(minutes=minutes)
                if cursor > now and not has_overlap(c, "tutor_id", tutor_id, cursor, end, TUTOR_BUFFER_MINUTES):
                    result.add(cursor.strftime("%H:%M"))
                cursor += timedelta(minutes=30)
    return sorted(result)
