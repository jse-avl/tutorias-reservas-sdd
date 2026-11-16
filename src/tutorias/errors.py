"""Errores de dominio. Cada uno lleva un código estable (ver specs/business-rules.md)."""


class DomainError(Exception):
    status = 400

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


class ValidationError(DomainError):
    status = 422


class ConflictError(DomainError):
    status = 409


class NotFoundError(DomainError):
    status = 404

    def __init__(self, message: str):
        super().__init__("NOT_FOUND", message)
