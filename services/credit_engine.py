def evaluate_application(data, score):

    if score < 500:
        return "rejected", "Score menor a 500."

    if data.age < 30 or data.age > 50:
        return "rejected", "Edad fuera del rango permitido."

    if data.monthly_income < 10000:
        return "rejected", "Ingreso mensual insuficiente."

    if data.bank_seniority_months < 6:
        return "rejected", "Antigüedad bancaria insuficiente."

    return "approved", "Solicitud aprobada. Cumple todas las reglas."   