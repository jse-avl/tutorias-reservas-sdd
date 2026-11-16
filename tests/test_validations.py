"""Pruebas unitarias de validaciones de usuario y reglas menores."""
import unittest

from helpers import NOW, TUE, setup
from tutorias import bookings, registry
from tutorias.errors import ConflictError, NotFoundError, ValidationError


class Validations(unittest.TestCase):
    def test_required_fields(self):
        db, *_ = setup()
        with self.assertRaises(ValidationError):
            registry.create_tutor(db, "  ", "Mat")
        with self.assertRaises(ValidationError):
            registry.create_student(db, "", "a@b.com")

    def test_duplicate_email(self):
        db, *_ = setup()
        with self.assertRaises(ConflictError):
            registry.create_student(db, "Otro", "LUIS@utp.ac.pa")

    def test_availability_validation(self):
        db, t, *_ = setup()
        for args in ((7, "09:00", "10:00"), (1, "9:00", "10:00"), (1, "10:00", "09:00")):
            with self.assertRaises(ValidationError):
                registry.add_availability(db, t["id"], *args)

    def test_invalid_start_minute(self):
        db, t, s1, _ = setup()
        with self.assertRaises(ValidationError) as cm:
            bookings.create_booking(db, t["id"], s1["id"], f"{TUE}T10:15", 30, NOW)
        self.assertEqual(cm.exception.code, "INVALID_START")

    def test_bad_datetime_format(self):
        db, t, s1, _ = setup()
        with self.assertRaises(ValidationError):
            bookings.create_booking(db, t["id"], s1["id"], "mañana", 30, NOW)

    def test_unknown_entities(self):
        db, t, s1, _ = setup()
        with self.assertRaises(NotFoundError):
            bookings.create_booking(db, 999, s1["id"], f"{TUE}T10:00", 30, NOW)
        with self.assertRaises(NotFoundError):
            bookings.cancel_booking(db, 999, NOW)

    def test_double_cancel(self):
        db, t, s1, _ = setup()
        b = bookings.create_booking(db, t["id"], s1["id"], f"{TUE}T10:00", 30, NOW)
        bookings.cancel_booking(db, b["id"], NOW)
        with self.assertRaises(ConflictError) as cm:
            bookings.cancel_booking(db, b["id"], NOW)
        self.assertEqual(cm.exception.code, "ALREADY_CANCELLED")


if __name__ == "__main__":
    unittest.main()
