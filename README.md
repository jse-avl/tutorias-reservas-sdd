# Sistema de Reservas de Tutorías Universitarias

Proyecto 2 — Tópicos Especiales II (Prof. Regis Rivera). Flujo: **ODD → SDD → código → pruebas → valor al usuario**.

## Equipo y roles (rotan por ciclo)
| Ciclo | Product / Spec Lead | Architecture / Dev Lead | QA / DevOps Lead |
|-------|--------------------|-------------------------|------------------|
| 1 — MVP | Jose Avila (Product/Spec) | Yireikis Abrego (Arch/Dev) | Christian Dutary (QA/DevOps) |
| 2 — Cambio de especificación | Christian Dutary | Jose Avila | Yireikis Abrego |

## Problema y outcome
Los estudiantes coordinan tutorías por mensajería y hay cruces de horario. **Outcome:** cero cruces y que el
estudiante encuentre y reserve cupos sin intervención del personal. Ver [specs/outcomes.md](specs/outcomes.md).

## Estado
- **25 pruebas** en verde con `python -m unittest discover -s tests`.
- **15 criterios de aceptación** (AC-01..AC-15) y **11 reglas de negocio** (BR-01..BR-11).
- Issues #1..#7 y su PR real por issue: ver [docs/pull-requests.md](docs/pull-requests.md).

## Ejecutar
Requiere solo Python 3.12 (sin dependencias).
```bash
python -m unittest discover -s tests          # pruebas (config en tests/helpers.py)
PYTHONPATH=src python -m tutorias --port 8000 # API
```
En PowerShell: `$env:PYTHONPATH="src"; python -m tutorias --port 8000`.

## Estructura
- `specs/` outcomes, requisitos, reglas, arquitectura, modelo, API, criterios de aceptación, plan
- `docs/` `ai-log.md`, `decisions.md`, `testing.md`, `issues.md`, `pull-requests.md`, `change-request-001.md` y `CHANGELOG.md`
- `src/tutorias/` código · `tests/` pruebas automatizadas

## Flujo de trabajo
Issue → rama `feature/N-...` → commits → PR (`docs/pull-requests.md`) → merge `--no-ff` a `main`.
Regla clave "no doble reserva": `tests/test_acceptance.py::test_AC01*` y `test_AC12*` (concurrencia).
