# Decisiones

- **D-01** Python + SQLite + `http.server` + `unittest`: cero dependencias, fácil de ejecutar/evaluar. Alternativa descartada: FastAPI (requiere instalación, no aporta al objetivo).
- **D-02** Dominio: tutorías universitarias (cercano al contexto del equipo, UTP).
- **D-03** Anti doble reserva en la capa de servicio con `BEGIN IMMEDIATE` + lock; SQLite no soporta restricción de solapamiento nativa.
- **D-04** `now` inyectable para pruebas deterministas.
- **D-05** Slots cada 30 min aunque la duración sea 60 (un tutor puede empezar a y media).
- **D-06 (cambio 001)** Buffer de 10 min entre tutorías del mismo tutor, ver `change-request-001.md`.
