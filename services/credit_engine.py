def evaluate_application(product_type:str, application, score: int, address_match: bool):

    
    if product_type == 'credito_personal':
        return evaluate_personal_loan(application, score, address_match)
    elif product_type == 'otro_tipo_credito':
        # Por si llegará a haber varios tipos de credito
        pass



def evaluate_personal_loan(application, score, address_match):
    reasons = []

    # Score crediticio
    if score is None:
        reasons.append("No se pudo obtener el score crediticio.")
    elif score < 500:
        reasons.append(
            f"El score crediticio ({score}) está por debajo del mínimo requerido (500)."
        )

    # Coincidencia de dirección
    if address_match is False:
        reasons.append(
            "La dirección extraída del documento no coincide con la dirección proporcionada."
        )

    # Ingreso mensual
    if application.monthly_income is None:
        reasons.append("No se proporcionó ingreso mensual.")
    elif application.monthly_income < 10000:
        reasons.append(
            f"El ingreso mensual (${application.monthly_income}) es menor al mínimo requerido ($10,000)."
        )

    # Rango de edad
    if application.age is None:
        reasons.append("No se proporcionó la edad del solicitante.")
    elif application.age < 30 or application.age > 50:
        reasons.append(
            f"La edad ({application.age}) está fuera del rango permitido (30 a 50 años)."
        )

    # Antigüedad bancaria mínima (12 meses)
    if application.bank_seniority_months is None:
        reasons.append("No se proporcionó la antigüedad bancaria.")
    elif application.bank_seniority_months < 12:
        reasons.append(
            f"La antigüedad bancaria ({application.bank_seniority_months} meses) es menor al mínimo requerido (12 meses)."
        )

    if reasons:
        return "RECHAZADO", " | ".join(reasons)

    return "APROBADO", "La solicitud cumple con todos los criterios crediticios establecidos."