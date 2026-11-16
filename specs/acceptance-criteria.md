# Criterios de aceptación (Given / When / Then)

Cada criterio tiene prueba automatizada en `tests/test_acceptance.py` (ID en el nombre del test).

- **AC-01 (BR-01, O1)** Dado un tutor con reserva 10:00–11:00, cuando otro estudiante reserva 10:30–11:00, entonces se rechaza con `TUTOR_CONFLICT`.
- **AC-02 (BR-02)** Dado un estudiante con reserva 10:00–11:00 con tutor A, cuando reserva 10:30 con tutor B, entonces `STUDENT_CONFLICT`.
- **AC-03 (BR-09)** Dada una reserva 10:00–11:00, cuando se reserva 11:00–11:30 con el mismo tutor, entonces se acepta.
- **AC-04 (BR-08)** Dada una reserva cancelada, cuando otro estudiante reserva el mismo horario, entonces se acepta.
- **AC-05 (RF-04, O2)** Dado un tutor disponible 09:00–12:00 con reserva 10:00–11:00, cuando se consultan slots de 60 min, entonces se devuelven `09:00` y `11:00`.
- **AC-06 (BR-03)** Duración 45 → `INVALID_DURATION`.
- **AC-07 (BR-04)** Reserva 11:30–12:30 con disponibilidad hasta 12:00 → `OUTSIDE_AVAILABILITY`.
- **AC-08 (BR-05)** Reserva en el pasado → `PAST_DATE`.
- **AC-09 (BR-06)** Un estudiante con 3 reservas en la semana intenta una cuarta → `WEEKLY_LIMIT`.
- **AC-10 (BR-07)** Cancelar con 1 h de anticipación → `TOO_LATE_TO_CANCEL`; con 3 h → aceptado.
- **AC-11 (RF-02)** Correo inválido → `VALIDATION`.
- **AC-12 (RNF-01)** 10 hilos reservando el mismo horario → exactamente 1 éxito.
