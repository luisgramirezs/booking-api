class ReservaError(Exception):
    """Clase base para errores de negocio relacionados con reservas."""
    pass


class HorarioInvalidoError(ReservaError):
    """El horario solicitado está fuera del rango permitido,
    o cae en domingo/festivo."""
    pass


class AnticipacionInsuficienteError(ReservaError):
    """La reserva se solicita con menos de 2 horas de anticipación."""
    pass


class SinDisponibilidadError(ReservaError):
    """El servicio/prestador no tiene cupo disponible en ese horario."""
    pass


class LimiteReservasActivasError(ReservaError):
    """El cliente ya alcanzó el máximo de reservas activas permitidas (3)."""
    pass