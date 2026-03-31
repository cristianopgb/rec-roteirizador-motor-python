"""
utils/numbers.py
Utilitários para manipulação e formatação de números.
"""
from typing import Union


def arredondar(valor: float, casas: int = 2) -> float:
    """Arredonda um float para o número de casas decimais especificado."""
    return round(valor, casas)


def to_float(valor: Union[str, int, float, None], padrao: float = 0.0) -> float:
    """
    Converte um valor para float de forma segura.

    Args:
        valor: Valor a converter.
        padrao: Valor retornado em caso de falha.

    Returns:
        Float convertido ou o valor padrão.
    """
    try:
        return float(valor)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return padrao


def percentual(parte: float, total: float) -> float:
    """
    Calcula o percentual de *parte* em relação a *total*.

    Returns:
        Percentual entre 0.0 e 100.0, ou 0.0 se total for zero.
    """
    if total == 0:
        return 0.0
    return round((parte / total) * 100, 2)
