def get_week_message(week: int) -> str:
    messages = {
        8: "Tudo ainda parece pequeno por fora, mas por dentro a vida já floresce com força.",
        12: "Seu bebê já começa a se mexer... mesmo que você ainda não sinta 🤍",
        16: "A cada semana, o invisível vai ganhando forma, presença e história.",
        20: "Agora já existe mais do que expectativa: existe vínculo, imaginação e presença.",
        24: "Seu corpo prepara abrigo. Seu coração prepara amor.",
        28: "Cada detalhe vivido hoje se tornará memória amanhã.",
        32: "Você já não está apenas esperando. Já está se encontrando com esse amor.",
        36: "Tudo parece mais próximo. O sonho já tem peso, tempo e verdade.",
        40: "Depois de tantas semanas de espera, amor e construção... o encontro está aqui.",
    }
    valid_weeks = sorted(messages.keys())
    selected = valid_weeks[0]
    for w in valid_weeks:
        if week >= w:
            selected = w
    return messages[selected]

def get_daily_moment() -> str:
    return "Hoje é mais um capítulo da sua história 🤍"
