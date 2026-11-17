# Cambio de especificación 001 (a mitad del desarrollo)

> Nota de transparencia: este cambio lo planteó el equipo/IA como ejercicio para demostrar el ciclo completo; no proviene de un cliente real. El profesor pedirá cambios adicionales en la presentación.

**Solicitud (inesperada):** "Los tutores necesitan 10 minutos entre tutorías para descansar y preparar material."

## Ciclo ejecutado
| Paso | Evidencia (commit en `feature/6-buffer-between-sessions`) |
|------|-----------|
| 1. Cambio solicitado | Este documento |
| 2. Actualizar especificación | `specs/business-rules.md` (BR-11), `specs/outcomes.md` (O6), `specs/requirements.md` (RF-08) |
| 3. Actualizar criterios de aceptación | `specs/acceptance-criteria.md`: AC-03 y AC-05 modificados, AC-13..AC-15 nuevos |
| 4. Actualizar plan/tareas | `specs/implementation-plan.md` (Ciclo 2, T6a–T6d) |
| 5. Modificar código | `bookings.py` (`has_overlap(buffer_minutes)`), `slots.py` |
| 6. Modificar pruebas | `tests/test_acceptance.py` (AC03, AC05, AC09 ajustados; AC13–AC15 nuevos) |
| 7. Resultados | 25 pruebas pasan (`python -m unittest discover -s tests`) |

## Impacto
- Un tutor con 10:00–11:00 ya no acepta 11:00 pero sí 11:30 (la grilla es de 30 min).
- Cambió el comportamiento de AC-03 y AC-05 (regresión consciente, documentada).
