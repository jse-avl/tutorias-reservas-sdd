# Requisitos

Cada requisito referencia el outcome que sirve.

| ID | Requisito | Outcome |
|----|-----------|---------|
| RF-01 | Registrar tutores (nombre, materia). | O2 |
| RF-02 | Registrar estudiantes (nombre, correo válido). | O3 |
| RF-03 | Definir disponibilidad semanal de un tutor (día de semana, hora inicio, hora fin). | O2 |
| RF-04 | Consultar horarios libres de un tutor en una fecha y duración (30/60 min). | O2 |
| RF-05 | Crear una reserva (tutor, estudiante, inicio, duración). | O1, O3 |
| RF-06 | Cancelar una reserva propia. | O3, O4 |
| RF-07 | Listar reservas de un estudiante. | O3 |
| RF-08 | (Cambio 001) El sistema aplica un buffer de 10 min entre reservas del mismo tutor, también al listar slots. | O6 |
| RNF-01 | Toda operación de reserva es atómica (sin condiciones de carrera). | O1 |
| RNF-02 | Errores devueltos con código y mensaje en español. | O3 |
| RNF-03 | Sin dependencias externas (solo biblioteca estándar de Python). | — |
