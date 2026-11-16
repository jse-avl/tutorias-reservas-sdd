# Estrategia de pruebas

Ejecutar: `PYTHONPATH=src:tests python -m unittest discover -s tests -v` (o `python -m unittest discover -s tests`, helpers ajusta `sys.path`).

| Archivo | Cubre |
|---------|-------|
| `tests/test_acceptance.py` | AC-01..AC-12 (+ AC-13..15 tras el cambio 001). **Incluye la regla obligatoria de no doble reserva (AC01, AC01b, AC12 concurrencia).** |
| `tests/test_validations.py` | Validaciones de usuario, entidades inexistentes, cancelación doble |
| `tests/test_api.py` | Flujo extremo a extremo y mapeo de errores a HTTP |

Trazabilidad: cada AC-xx en `specs/acceptance-criteria.md` ↔ test con el mismo ID en el nombre.
