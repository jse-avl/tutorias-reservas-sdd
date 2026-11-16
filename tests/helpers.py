import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from tutorias import registry  # noqa: E402
from tutorias.db import Database  # noqa: E402

# Lunes 2026-11-16 08:00. El martes 17 es weekday=1.
NOW = datetime(2026, 11, 16, 8, 0)
TUE = "2026-11-17"
WED = "2026-11-18"


def setup(window=("09:00", "12:00"), weekday=1):
    db = Database()
    tutor = registry.create_tutor(db, "Ana Pérez", "Cálculo")
    registry.add_availability(db, tutor["id"], weekday, *window)
    s1 = registry.create_student(db, "Luis", "luis@utp.ac.pa")
    s2 = registry.create_student(db, "María", "maria@utp.ac.pa")
    return db, tutor, s1, s2
