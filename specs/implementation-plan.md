# Plan de implementación

Roles rotan por ciclo (ver `docs/ai-log.md`). Cada tarea = un Issue (`docs/issues.md`) = una rama = un PR.

## Ciclo 1 — MVP
| Tarea | Issue | Rama | Depende de |
|-------|-------|------|-----------|
| T1 Esquema SQLite + registro de tutores/estudiantes/disponibilidad | #1 | `feature/1-core-data` | — |
| T2 Consulta de slots libres | #2 | `feature/2-slots` | T1 |
| T3 Reserva con reglas BR-01..BR-10 + cancelación | #3 | `feature/3-booking-rules` | T1 |
| T4 API HTTP | #4 | `feature/4-http-api` | T2, T3 |
| T5 Pruebas de aceptación y concurrencia | #5 | `feature/5-acceptance-tests` | T3 |

## Ciclo 2 — Cambio de especificación (mitad del proyecto)
Ver `docs/change-request-001.md`. Issue #6, rama `feature/6-buffer-between-sessions`.
