# Reglas de negocio

| ID | Regla | Error |
|----|-------|-------|
| BR-01 | **No doble reserva (tutor):** un tutor no puede tener dos reservas `confirmed` cuyos intervalos se solapen. | 409 `TUTOR_CONFLICT` |
| BR-02 | **No doble reserva (estudiante):** un estudiante no puede tener dos reservas `confirmed` solapadas. | 409 `STUDENT_CONFLICT` |
| BR-03 | La duración debe ser 30 o 60 minutos. | 422 `INVALID_DURATION` |
| BR-04 | La reserva debe caer completa dentro de una ventana de disponibilidad del tutor ese día. | 422 `OUTSIDE_AVAILABILITY` |
| BR-05 | No se puede reservar en el pasado. | 422 `PAST_DATE` |
| BR-06 | Un estudiante tiene como máximo 3 reservas `confirmed` por semana calendario (lunes–domingo). | 409 `WEEKLY_LIMIT` |
| BR-07 | Cancelar requiere al menos 2 horas de anticipación al inicio. | 409 `TOO_LATE_TO_CANCEL` |
| BR-08 | Una reserva cancelada libera el horario inmediatamente. | — |
| BR-09 | Intervalos son semiabiertos `[inicio, fin)`: una reserva que termina 10:00 y otra que inicia 10:00 NO se solapan. | — |
| BR-10 | Inicios en múltiplos de 30 minutos. | 422 `INVALID_START` |
