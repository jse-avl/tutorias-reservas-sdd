# Arquitectura

## Libertad tecnológica (decisión)
- **Lenguaje:** Python 3.12
- **Base de datos:** SQLite (módulo `sqlite3`, estándar)
- **API:** HTTP/JSON con `http.server` (estándar)
- **Pruebas:** `unittest` (estándar)
- **Justificación:** cero dependencias → el proyecto corre en cualquier máquina con `python -m unittest`.
  Ver también `docs/decisions.md` (D-01).

## Capas
```
 HTTP (api.py)  ->  Dominio (registry.py / slots.py / bookings.py)  ->  SQLite (db.py)
   JSON/errores        reglas BR-xx, validaciones                        schema, transacciones
```
- El dominio no conoce HTTP: es testeable de forma aislada. `registry.py` registra tutores, estudiantes y
  disponibilidad; `slots.py` calcula horarios libres; `bookings.py` aplica las reglas BR-xx de reserva y
  cancelación. Las funciones de reserva reciben `now` por parámetro para pruebas deterministas.
- `api.py` traduce excepciones de dominio a códigos HTTP (ValidationError→422, ConflictError→409, NotFoundError→404).
- Atomicidad (RNF-01): cada reserva corre dentro de `Database.tx()` (`db.py`), que usa `BEGIN IMMEDIATE` +
  `threading.Lock`; verificar-conflicto e insertar son una sola sección crítica.

## Ejecución
`python -m tutorias --port 8000` (ver README).
