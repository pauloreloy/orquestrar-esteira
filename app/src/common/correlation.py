import contextvars


correlation_id_var = contextvars.ContextVar("correlation_id", default=None)


def set_correlation_id(value):
    correlation_id_var.set(value)


def get_correlation_id():
    return correlation_id_var.get()