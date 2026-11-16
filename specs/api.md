# API (HTTP/JSON)

| Método | Ruta | Cuerpo / query | Éxito |
|--------|------|----------------|-------|
| POST | `/tutors` | `{name, subject}` | 201 tutor |
| POST | `/students` | `{name, email}` | 201 estudiante |
| POST | `/tutors/{id}/availability` | `{weekday, start_time, end_time}` | 201 |
| GET | `/tutors/{id}/slots` | `?date=YYYY-MM-DD&minutes=30\|60` | 200 `{slots:[ "HH:MM", ...]}` |
| POST | `/bookings` | `{tutor_id, student_id, start, minutes}` | 201 reserva |
| POST | `/bookings/{id}/cancel` | — | 200 reserva |
| GET | `/bookings` | `?student_id=` | 200 lista |

Errores: `{"error": {"code": "TUTOR_CONFLICT", "message": "..."}}` con 404/409/422 (ver `business-rules.md`).
