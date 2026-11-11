class FoodStoreError(Exception):
    """Excepción base para todas las excepciones del dominio Food Store."""
    pass

class EntidadNoEncontradaError(FoodStoreError):
    """Se lanza cuando un objeto buscado por ID no existe o está eliminado."""
    pass

class DatoInvalidoError(FoodStoreError):
    """Se lanza cuando los datos ingresados no cumplen el formato o las restricciones requeridas."""
    pass

class PrecioInvalidoError(DatoInvalidoError):
    """Se lanza cuando el precio ingresado es menor a cero."""
    pass

class StockInsuficienteError(FoodStoreError):
    """Se lanza cuando la cantidad solicitada supera el stock disponible."""
    pass

class DuplicadoError(FoodStoreError):
    """Se lanza cuando se intenta registrar un elemento duplicado (ej. mail o categoría repetida)."""
    pass

class OperacionNoPermitidaError(FoodStoreError):
    """Se lanza ante acciones prohibidas por regla de negocio (ej. transiciones inválidas)."""
    pass

class CredencialesInvalidasError(FoodStoreError):
    """Se lanza cuando falla el inicio de sesión."""
    pass