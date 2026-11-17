# Estrategia de pruebas

Ejecutar desde la raíz: `python -m unittest discover -s tests -v` (`tests/helpers.py` ajusta `sys.path`, no hace falta `PYTHONPATH`).
Total: **25 pruebas** (16 de aceptación en `test_acceptance.py`, incluida AC-12 de concurrencia).

| Archivo | Cubre |
|---------|-------|
| `tests/test_acceptance.py` | AC-01..AC-12 (+ AC-13..15 tras el cambio 001). **Incluye la regla obligatoria de no doble reserva (AC01, AC01b, AC12 concurrencia).** |
| `tests/test_validations.py` | Validaciones de usuario, entidades inexistentes, cancelación doble |
| `tests/test_api.py` | Flujo extremo a extremo y mapeo de errores a HTTP |

Trazabilidad: cada AC-xx en `specs/acceptance-criteria.md` ↔ test con el mismo ID en el nombre.
