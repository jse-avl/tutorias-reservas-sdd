# AI Development Log

Roles: **Jose** = Product/Spec Lead · **Yire** = Architecture/Dev Lead · **Chris** = QA/DevOps Lead (ciclo 1).
Ciclo 2 (cambio 001) rota: Chris = Spec, Jose = Dev, Yire = QA.

| # | Actividad | IA utilizada | Solicitud | Resultado | Decisión / verificación humana |
|---|-----------|--------------|-----------|-----------|--------------------------------|
| 1 | Lectura del enunciado | Claude Code (agente de escritorio) | Leer el PDF del proyecto y desarrollarlo | Resumen de requisitos y estructura de entrega | Jose pidió "desarrolla el proyecto según el PDF". La IA eligió el dominio *Tutorías universitarias* (D-02) y Jose lo aceptó al continuar. |
| 2 | ODD | Claude Code | Redactar problema, preguntas de exploración y outcomes | `specs/outcomes.md` | Propuesto por la IA. **Pendiente:** validación de Jose como Product Lead (ver PR #15). |
| 3 | SDD | Claude Code | Convertir outcomes en requisitos, reglas, API, criterios y plan | `specs/*.md` | Propuesto por la IA (límite semanal 3, cancelación 2 h, slots de 30 min). **Pendiente:** validación de Jose. |
| 4 | Implementación | Claude Code | Implementar servicio, SQLite y API según specs | `src/tutorias/*` | Generado por la IA. Revisado por Yire (registrado el 2026-11-16 en «Verificación humana»). |
| 5 | Pruebas | Claude Code | Un test por criterio de aceptación + concurrencia | `tests/*` | Generado por la IA. Un test falló por expectativa errónea (slots cada 30 min): se corrigió el test, no el código (D-05). Revisado por Chris (registrado el 2026-11-16 en «Verificación humana»). |
| 6 | Cambio de spec 001 | Claude Code | Aplicar buffer de 10 min siguiendo el ciclo spec→código | `docs/change-request-001.md` | El cambio fue planteado como ejercicio por la IA/Jose para demostrar el ciclo. Revisado por Yire como QA del ciclo 2 (registrado el 2026-11-16). |
| 7 | Publicación en GitHub | Claude Code | Crear repo, issues y PR | Repo `tutorias-reservas-sdd`, issues #1–#7, PR #15 y #16 | Jose autorizó; Yire y Chris facilitaron tokens y solo se usaron para crear/ver elementos propios de su rol. |
| 8 | Corrección de trazabilidad y coherencia documental | OpenCode (modelo Big Pickle) | Revisar que README, `docs/` y `specs/` coincidan y enlazar cada issue con su PR real | PR #17 (autoría de #13/#14), PR #18 (coherencia docs/specs), comentarios nuevos en issues #1–#7 | Jose solicitó la revisión; se verificaron las cifras (25 pruebas, 15 AC, BR-01..BR-11) contra el código. No se usaron tokens de Yire ni de Chris para aprobar. |
| 9 | Registro de la verificación humana | OpenCode (modelo Big Pickle) | Dejar constancia de que Yire y Chris ya revisaron aunque no tenían acceso a su computadora | PR #19: casillas de Yire y Chris marcadas con nota de procedencia; `docs/pull-requests.md` separa revisión humana de approval en GitHub | Jose confirmó que ambos revisaron lo que les corresponde. Se registra por confirmación; el approval formal en GitHub sigue pendiente y no se emitieron approvals con sus cuentas. |

## Verificación humana (completar con revisiones reales)
- [ ] Jose revisó outcomes/specs
- [x] Yire revisó arquitectura y código — confirmado por Yire y registrado por Jose el 2026-11-16. No hay approval en GitHub porque Yire no tenía acceso a su computadora.
- [x] Chris revisó pruebas y ejecutó la suite — confirmado por Chris y registrado por Jose el 2026-11-16. No hay approval en GitHub porque Chris no tenía acceso a su computadora.

> Las casillas se marcan solo con revisiones reales. Las de Yire y Chris provienen de su confirmación; el approval formal en GitHub quedó pendiente por falta de acceso a sus equipos y pueden emitirlo cuando lo recuperen.
