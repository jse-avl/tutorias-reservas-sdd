# Modelo de datos

```
tutors(id PK, name, subject)
availability(id PK, tutor_id FK, weekday 0-6 [0=lunes], start_time 'HH:MM', end_time 'HH:MM')
students(id PK, name, email UNIQUE)
bookings(id PK, tutor_id FK, student_id FK, start 'YYYY-MM-DDTHH:MM', end 'YYYY-MM-DDTHH:MM',
         status 'confirmed'|'cancelled', created_at)
```
- Fechas ISO 8601 sin zona (hora local de campus); comparables lexicográficamente.
- Índices: `bookings(tutor_id, start)`, `bookings(student_id, start)`.
- Solo `status='confirmed'` bloquea horarios.
