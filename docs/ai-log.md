# AI Development Log

| # | Actividad | IA utilizada | Solicitud | Resultado | Decisión |
|---|-----------|--------------|-----------|-----------|----------|
| 1 | Lectura del enunciado | Claude Code (agente CLI/desktop) | Leer el PDF del proyecto y desarrollarlo | Resumen de requisitos y estructura de entrega | Elegir dominio Tutorías universitarias |
| 2 | ODD | Claude Code | Redactar problema, preguntas de exploración y outcomes | `specs/outcomes.md` | Revisado por Product Lead (Jose); se aceptan O1–O5 |
| 3 | SDD | Claude Code | Convertir outcomes en requisitos, reglas, API, criterios Given/When/Then, plan | `specs/*.md` | Aceptado; se fijó límite semanal 3 y cancelación 2 h |
| 4 | Implementación | Claude Code | Implementar servicio, SQLite y API según specs | `src/tutorias/*` | Aceptado tras revisión de Dev Lead (Yireikis) |
| 5 | Pruebas | Claude Code | Un test por criterio de aceptación + concurrencia | `tests/*` | Un test falló por expectativa errónea (slots cada 30 min): se corrigió el test, no el código (D-05) |
| 6 | Cambio de spec 001 | Claude Code | Aplicar buffer de 10 min siguiendo el ciclo spec→código | Ver `change-request-001.md` | Aceptado tras revisión de QA (Yireikis) |

> Nota: los equipos deben añadir aquí cualquier uso adicional de IA y la verificación humana realizada.
