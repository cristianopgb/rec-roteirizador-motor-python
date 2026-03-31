"""
utils/dates.py
Utilitários para manipulação e formatação de datas e horários.
"""
from datetime import date, datetime, timezone
from typing import Optional


def agora_utc() -> datetime:
    """Retorna o datetime atual em UTC."""
    return datetime.now(tz=timezone.utc)


def formatar_data(dt: datetime, fmt: str = "%d/%m/%Y %H:%M:%S") -> str:
    """
    Formata um objeto datetime para string.

    Args:
        dt: Objeto datetime a formatar.
        fmt: Formato de saída (padrão: DD/MM/YYYY HH:MM:SS).

    Returns:
        String formatada.
    """
    return dt.strftime(fmt)


def parse_data(texto: str, fmt: str = "%Y-%m-%dT%H:%M:%S") -> Optional[datetime]:
    """
    Faz o parse de uma string para datetime.

    Args:
        texto: String com a data.
        fmt: Formato esperado.

    Returns:
        Objeto datetime ou None em caso de falha.
    """
    try:
        return datetime.strptime(texto, fmt)
    except (ValueError, TypeError):
        return None


def dentro_janela(dt: datetime, inicio: Optional[datetime], fim: Optional[datetime]) -> bool:
    """
    Verifica se um datetime está dentro de uma janela de tempo.

    Args:
        dt: Datetime a verificar.
        inicio: Início da janela (inclusive). None = sem restrição.
        fim: Fim da janela (inclusive). None = sem restrição.

    Returns:
        True se *dt* está dentro da janela.
    """
    if inicio is not None and dt < inicio:
        return False
    if fim is not None and dt > fim:
        return False
    return True
