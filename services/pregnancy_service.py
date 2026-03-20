# services/pregnancy_service.py
# Responsável por cálculos relacionados à gestação:
# - semana atual
# - data prevista do parto
# - tamanho do bebê por semana

from datetime import datetime, date, timedelta


def calculate_current_week(config: dict) -> int:
    """
    Calcula a semana atual da gravidez a partir das configurações da usuária.

    Prioridade:
    1) Se método = DUM → calcula DPP = DUM + 280 dias
    2) Caso contrário → usa DPP diretamente

    Retorna um número entre 1 e 40.
    """

    metodo = (config.get("metodo_data") or "DPP").upper()

    # Caso a usuária tenha informado a DUM
    if metodo == "DUM":
        dum_str = config.get("data_ultima_menstruacao", "")
        dum = _parse_date(dum_str)

        if dum:
            dpp = dum + timedelta(days=280)
            return _week_from_due_date(dpp)

    # Fallback: usar diretamente a data prevista do parto (DPP)
    dpp_str = config.get("data_prevista_parto", "")
    dpp = _parse_date(dpp_str)

    if dpp:
        return _week_from_due_date(dpp)

    # Último fallback de segurança
    return 1


def _week_from_due_date(due_date: date) -> int:
    """
    Calcula a semana atual com base na data prevista do parto.
    """
    today = date.today()
    days_until_due = (due_date - today).days

    # 280 dias é a duração média da gestação
    gestation_days = 280 - days_until_due

    # Garante intervalo seguro entre 1 e 40 semanas
    week = max(1, min(40, gestation_days // 7))
    return week


def _parse_date(value: str):
    """
    Converte uma string YYYY-MM-DD em objeto date.
    Retorna None se o valor for inválido ou vazio.
    """
    if not value:
        return None

    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def get_baby_size(week: int) -> str:
    """
    Retorna uma comparação simbólica do tamanho do bebê
    de acordo com a semana da gravidez.
    """

    sizes = {
        8: "🍇 Do tamanho de uma uva",
        12: "🍋 Do tamanho de um limão",
        16: "🥑 Do tamanho de um abacate",
        20: "🍌 Do tamanho de uma banana",
        24: "🌽 Do tamanho de um milho",
        28: "🥥 Do tamanho de um coco",
        32: "🍍 Do tamanho de um abacaxi pequeno",
        36: "🥬 Do tamanho de uma alface",
        40: "🎀 Pronto para chegar",
    }

    # Seleciona o maior marco <= semana atual
    valid_weeks = sorted(sizes.keys())
    selected = valid_weeks[0]

    for w in valid_weeks:
        if week >= w:
            selected = w

    return sizes[selected]