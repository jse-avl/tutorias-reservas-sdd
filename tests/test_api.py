import unittest

from helpers import NOW, TUE
from tutorias.api import make_app
from tutorias.db import Database


class ApiFlow(unittest.TestCase):
    def setUp(self):
        self.h = make_app(Database(), clock=lambda: NOW)

    def call(self, method, path, body=None, query=None):
        return self.h(method, path, query or {}, body or {})

    def test_end_to_end_flow_and_conflict_status(self):
        _, tutor = self.call("POST", "/tutors", {"name": "Ana", "subject": "Cálculo"})
        _, s1 = self.call("POST", "/students", {"name": "Luis", "email": "l@utp.ac.pa"})
        _, s2 = self.call("POST", "/students", {"name": "Mar", "email": "m@utp.ac.pa"})
        self.assertEqual(self.call("POST", f"/tutors/{tutor['id']}/availability",
                                   {"weekday": 1, "start_time": "09:00", "end_time": "12:00"})[0], 201)
        st, body = self.call("GET", f"/tutors/{tutor['id']}/slots", query={"date": [TUE], "minutes": ["60"]})
        self.assertEqual((st, body["slots"]), (200, ["09:00", "09:30", "10:00", "10:30", "11:00"]))
        req = {"tutor_id": tutor["id"], "student_id": s1["id"], "start": f"{TUE}T10:00", "minutes": 60}
        self.assertEqual(self.call("POST", "/bookings", req)[0], 201)
        st, body = self.call("POST", "/bookings", {**req, "student_id": s2["id"]})
        self.assertEqual((st, body["error"]["code"]), (409, "TUTOR_CONFLICT"))
        st, body = self.call("GET", "/bookings", query={"student_id": [str(s1["id"])]})
        self.assertEqual((st, len(body)), (200, 1))

    def test_errors_map_to_http(self):
        self.assertEqual(self.call("POST", "/students", {"name": "x", "email": "mal"})[0], 422)
        self.assertEqual(self.call("GET", "/nope")[0], 404)
        self.assertEqual(self.call("POST", "/bookings/99/cancel")[0], 404)


if __name__ == "__main__":
    unittest.main()
