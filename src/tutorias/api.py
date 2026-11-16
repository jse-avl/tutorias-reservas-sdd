"""API HTTP/JSON (specs/api.md). Traduce errores de dominio a códigos HTTP."""
import json
import re
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from . import bookings, registry, slots
from .db import Database
from .errors import DomainError, NotFoundError, ValidationError


def make_app(db, clock=datetime.now):
    """Devuelve handle(method, path, query, body) -> (status, payload). Testeable sin red."""

    def handle(method, path, query, body):
        now = clock().replace(second=0, microsecond=0)
        try:
            if method == "POST" and path == "/tutors":
                return 201, registry.create_tutor(db, body.get("name"), body.get("subject"))
            if method == "POST" and path == "/students":
                return 201, registry.create_student(db, body.get("name"), body.get("email"))
            m = re.fullmatch(r"/tutors/(\d+)/availability", path)
            if method == "POST" and m:
                return 201, registry.add_availability(
                    db, int(m[1]), body.get("weekday"), body.get("start_time"), body.get("end_time"))
            m = re.fullmatch(r"/tutors/(\d+)/slots", path)
            if method == "GET" and m:
                try:
                    minutes = int(query.get("minutes", ["60"])[0])
                except ValueError:
                    raise ValidationError("INVALID_DURATION", "minutes debe ser numérico.")
                date = query.get("date", [None])[0]
                return 200, {"slots": slots.free_slots(db, int(m[1]), date, minutes, now)}
            if method == "POST" and path == "/bookings":
                return 201, bookings.create_booking(
                    db, body.get("tutor_id"), body.get("student_id"),
                    body.get("start"), body.get("minutes"), now)
            m = re.fullmatch(r"/bookings/(\d+)/cancel", path)
            if method == "POST" and m:
                return 200, bookings.cancel_booking(db, int(m[1]), now)
            if method == "GET" and path == "/bookings":
                sid = query.get("student_id", [""])[0]
                if not sid.isdigit():
                    raise ValidationError("VALIDATION", "student_id es obligatorio.")
                return 200, bookings.list_bookings(db, int(sid))
            raise NotFoundError("Ruta no encontrada.")
        except DomainError as e:
            return e.status, {"error": {"code": e.code, "message": e.message}}

    return handle


def serve(port=8000, db_path="tutorias.db"):
    handle = make_app(Database(db_path))

    class Handler(BaseHTTPRequestHandler):
        def _do(self, method):
            url = urlparse(self.path)
            body = {}
            length = int(self.headers.get("Content-Length") or 0)
            if length:
                try:
                    body = json.loads(self.rfile.read(length))
                    if not isinstance(body, dict):
                        raise ValueError
                except ValueError:
                    return self._send(422, {"error": {"code": "VALIDATION", "message": "JSON inválido."}})
            self._send(*handle(method, url.path, parse_qs(url.query), body))

        def _send(self, status, payload):
            data = json.dumps(payload, ensure_ascii=False).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self): self._do("GET")
        def do_POST(self): self._do("POST")
        def log_message(self, *a): pass

    srv = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"Tutorías API en http://127.0.0.1:{port}")
    srv.serve_forever()
