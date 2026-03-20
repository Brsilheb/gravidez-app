from datetime import datetime, date

def calculate_current_week(due_date_str: str) -> int:
    due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
    today = date.today()
    days_until_due = (due_date - today).days
    gestation_days = 280 - days_until_due
    week = max(1, min(40, gestation_days // 7))
    return week

def get_baby_size(week: int) -> str:
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
    valid_weeks = sorted(sizes.keys())
    selected = valid_weeks[0]
    for w in valid_weeks:
        if week >= w:
            selected = w
    return sizes[selected]
