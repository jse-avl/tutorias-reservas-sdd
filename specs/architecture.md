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
 HTTP (api.py)  ->  Servicio de dominio (service.py)  ->  SQLite (schema en service.py)
   JSON/errores        reglas BR-xx, atomicidad             tutors, availability, students, bookings
```
- `service.py` no conoce HTTP: es testeable de forma aislada. Recibe `now` por parámetro para pruebas deterministas.
- `api.py` traduce excepciones de dominio a códigos HTTP (ValidationError→422, ConflictError→409, NotFoundError→404).
- Atomicidad (RNF-01): cada reserva corre dentro de `BEGIN IMMEDIATE` + `threading.Lock`, por lo que
  verificar-conflicto e insertar son una sola sección crítica.

## Ejecución
`python -m tutorias --port 8000` (ver README).
