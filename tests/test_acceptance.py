"""Un test por criterio de aceptación (specs/acceptance-criteria.md)."""
import threading
import unittest

from helpers import NOW, TUE, WED, setup
from tutorias import bookings, registry, slots
from tutorias.errors import ConflictError, ValidationError


def book(db, t, s, start, minutes=60, now=NOW):
    return bookings.create_booking(db, t["id"], s["id"], start, minutes, now)


class Acceptance(unittest.TestCase):
    def test_AC01_no_double_booking_tutor(self):
        db, t, s1, s2 = setup()
        book(db, t, s1, f"{TUE}T10:00")
        with self.assertRaises(ConflictError) as cm:
            book(db, t, s2, f"{TUE}T10:30", 30)
        self.assertEqual(cm.exception.code, "TUTOR_CONFLICT")

    def test_AC01b_exact_same_slot_rejected(self):
        db, t, s1, s2 = setup()
        book(db, t, s1, f"{TUE}T10:00")
        with self.assertRaises(ConflictError) as cm:
            book(db, t, s2, f"{TUE}T10:00")
        self.assertEqual(cm.exception.code, "TUTOR_CONFLICT")

    def test_AC02_student_cannot_overlap_with_other_tutor(self):
        db, t, s1, _ = setup()
        t2 = registry.create_tutor(db, "Beto", "Física")
        registry.add_availability(db, t2["id"], 1, "09:00", "12:00")
        book(db, t, s1, f"{TUE}T10:00")
        with self.assertRaises(ConflictError) as cm:
            book(db, t2, s1, f"{TUE}T10:30", 30)
        self.assertEqual(cm.exception.code, "STUDENT_CONFLICT")

    def test_AC03_adjacent_bookings_allowed(self):
        db, t, s1, s2 = setup()
        book(db, t, s1, f"{TUE}T10:00")
        b = book(db, t, s2, f"{TUE}T11:30", 30)  # cambio 001: antes 11:00
        self.assertEqual(b["status"], "confirmed")

    def test_AC04_cancelled_slot_is_released(self):
        db, t, s1, s2 = setup()
        b = book(db, t, s1, f"{TUE}T10:00")
        bookings.cancel_booking(db, b["id"], NOW)
        self.assertEqual(book(db, t, s2, f"{TUE}T10:00")["student_id"], s2["id"])

    def test_AC05_free_slots_exclude_booked(self):
        db, t, s1, _ = setup(("09:00", "13:00"))
        book(db, t, s1, f"{TUE}T10:00")
        self.assertEqual(slots.free_slots(db, t["id"], TUE, 60, NOW), ["11:30", "12:00"])

    def test_AC06_invalid_duration(self):
        db, t, s1, _ = setup()
        with self.assertRaises(ValidationError) as cm:
            book(db, t, s1, f"{TUE}T10:00", 45)
        self.assertEqual(cm.exception.code, "INVALID_DURATION")

    def test_AC07_outside_availability(self):
        db, t, s1, _ = setup()
        with self.assertRaises(ValidationError) as cm:
            book(db, t, s1, f"{TUE}T11:30")
        self.assertEqual(cm.exception.code, "OUTSIDE_AVAILABILITY")
        with self.assertRaises(ValidationError):  # día sin disponibilidad
            book(db, t, s1, f"{WED}T10:00")

    def test_AC08_past_date(self):
        db, t, s1, _ = setup()
        with self.assertRaises(ValidationError) as cm:
            book(db, t, s1, "2026-11-10T10:00")
        self.assertEqual(cm.exception.code, "PAST_DATE")

    def test_AC09_weekly_limit(self):
        db, t, s1, _ = setup(("08:00", "18:00"))
        for h in ("08:00", "09:30", "11:00"):  # cambio 001: huecos de buffer
            book(db, t, s1, f"{TUE}T{h}")
        with self.assertRaises(ConflictError) as cm:
            book(db, t, s1, f"{TUE}T12:30")
        self.assertEqual(cm.exception.code, "WEEKLY_LIMIT")

    def test_AC10_cancellation_policy(self):
        db, t, s1, _ = setup()
        b = book(db, t, s1, f"{TUE}T10:00")
        with self.assertRaises(ConflictError) as cm:
            bookings.cancel_booking(db, b["id"], bookings.parse_dt(f"{TUE}T09:00"))
        self.assertEqual(cm.exception.code, "TOO_LATE_TO_CANCEL")
        ok = bookings.cancel_booking(db, b["id"], bookings.parse_dt(f"{TUE}T07:00"))
        self.assertEqual(ok["status"], "cancelled")

    def test_AC11_invalid_email(self):
        db, *_ = setup()
        for bad in ("sin-arroba", "a@b", "", None):
            with self.assertRaises(ValidationError):
                registry.create_student(db, "X", bad)

    def test_AC12_concurrent_requests_single_winner(self):
        db, t, _, _ = setup()
        students = [registry.create_student(db, f"E{i}", f"e{i}@utp.ac.pa") for i in range(10)]
        results = []

        def attempt(s):
            try:
                book(db, t, s, f"{TUE}T10:00")
                results.append("ok")
            except ConflictError:
                results.append("conflict")

        threads = [threading.Thread(target=attempt, args=(s,)) for s in students]
        [th.start() for th in threads]
        [th.join() for th in threads]
        self.assertEqual(results.count("ok"), 1)
        self.assertEqual(results.count("conflict"), 9)

    def test_AC13_buffer_rejects_adjacent_same_tutor(self):
        db, t, s1, s2 = setup()
        book(db, t, s1, f"{TUE}T10:00")
        with self.assertRaises(ConflictError) as cm:
            book(db, t, s2, f"{TUE}T11:00", 30)
        self.assertEqual(cm.exception.code, "TUTOR_CONFLICT")

    def test_AC14_buffer_applies_before_booking_too(self):
        db, t, s1, s2 = setup()
        book(db, t, s1, f"{TUE}T10:00")
        self.assertEqual(book(db, t, s2, f"{TUE}T09:00", 30)["status"], "confirmed")
        s3 = registry.create_student(db, "Pedro", "pedro@utp.ac.pa")
        with self.assertRaises(ConflictError):
            book(db, t, s3, f"{TUE}T09:30", 30)

    def test_AC15_buffer_not_applied_across_tutors(self):
        db, t, s1, _ = setup()
        t2 = registry.create_tutor(db, "Beto", "Física")
        registry.add_availability(db, t2["id"], 1, "09:00", "12:00")
        book(db, t, s1, f"{TUE}T10:00")
        self.assertEqual(book(db, t2, s1, f"{TUE}T11:00", 30)["status"], "confirmed")


if __name__ == "__main__":
    unittest.main()
