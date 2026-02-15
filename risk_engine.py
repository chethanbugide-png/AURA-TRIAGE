import random

def calculate_risk(age, bp, hr, temp, conditions, symptoms):

    score = 0
    reasoning = []
    critical_flags = []
    factor_weights = []

    # ---------------- AGE ----------------
    if age >= 75:
        score += 4
        reasoning.append("advanced geriatric vulnerability")
        factor_weights.append(("Age", 4))
    elif age >= 60:
        score += 3
        reasoning.append("high age-associated cardiovascular risk")
        factor_weights.append(("Age", 3))
    elif age >= 40:
        score += 1
        reasoning.append("moderate age-related factor")
        factor_weights.append(("Age", 1))

    # ---------------- BLOOD PRESSURE ----------------
    if bp >= 180:
        score += 5
        critical_flags.append("hypertensive crisis state")
        factor_weights.append(("Blood Pressure", 5))
    elif bp >= 160:
        score += 3
        reasoning.append("severe hypertension")
        factor_weights.append(("Blood Pressure", 3))
    elif bp >= 140:
        score += 2
        reasoning.append("elevated blood pressure")
        factor_weights.append(("Blood Pressure", 2))

    # ---------------- HEART RATE ----------------
    if hr >= 140:
        score += 5
        critical_flags.append("extreme tachycardia")
        factor_weights.append(("Heart Rate", 5))
    elif hr >= 120:
        score += 3
        reasoning.append("tachycardic response")
        factor_weights.append(("Heart Rate", 3))
    elif hr >= 100:
        score += 1
        reasoning.append("elevated heart rate")
        factor_weights.append(("Heart Rate", 1))

    # ---------------- TEMPERATURE ----------------
    if temp >= 104:
        score += 4
        critical_flags.append("hyperpyrexia condition")
        factor_weights.append(("Temperature", 4))
    elif temp >= 101:
        score += 2
        reasoning.append("febrile inflammatory response")
        factor_weights.append(("Temperature", 2))

    # ---------------- SYMPTOMS ----------------
    for s in symptoms:

        if s == "Chest Pain":
            score += 5
            critical_flags.append("possible acute coronary syndrome")
            factor_weights.append(("Chest Pain", 5))

        elif s == "Stroke Signs":
            score += 6
            critical_flags.append("probable cerebrovascular accident")
            factor_weights.append(("Stroke Signs", 6))

        elif s == "Loss of Consciousness":
            score += 6
            critical_flags.append("neurological instability")
            factor_weights.append(("Loss of Consciousness", 6))

        elif s == "Shortness of Breath":
            score += 3
            reasoning.append("respiratory compromise")
            factor_weights.append(("Shortness of Breath", 3))

        elif s == "Severe Headache":
            score += 2
            reasoning.append("neurological distress indicator")
            factor_weights.append(("Severe Headache", 2))

        else:
            score += 1
            factor_weights.append((s, 1))

    # ---------------- CONDITIONS ----------------
    for c in conditions:

        if c in ["Heart Disease", "Hypertension"]:
            score += 3
            reasoning.append("underlying cardiovascular disease")
            factor_weights.append((c, 3))

        elif c == "Diabetes":
            score += 2
            reasoning.append("metabolic comorbidity")
            factor_weights.append((c, 2))

        elif c == "Cancer":
            score += 3
            reasoning.append("immunocompromised state")
            factor_weights.append((c, 3))

        else:
            score += 1
            factor_weights.append((c, 1))

    # ---------------- SEVERITY NORMALIZATION ----------------
    severity_index = min(100, score * 6)  # scaled to 0-100

    # Logistic-like probability simulation
    probability = round(min(0.99, 0.55 + (score / 40)), 4)

    # ---------------- RISK CLASSIFICATION ----------------
    if critical_flags or score >= 14:
        risk = "Critical Priority"
        priority = "PRIORITY 1 - IMMEDIATE CARE"
        department = "Emergency / Specialist Intervention"
        wait_time = "0 - 5 minutes"

    elif score >= 8:
        risk = "Moderate Attention"
        priority = "PRIORITY 2 - URGENT CARE"
        department = "Specialist Evaluation"
        wait_time = "10 - 30 minutes"

    else:
        risk = "Stable"
        priority = "PRIORITY 3 - ROUTINE CARE"
        department = "General Physician"
        wait_time = "30 - 60 minutes"

    # ---------------- TRUE DYNAMIC EXPLANATION ----------------
    if risk == "Critical Priority":

        explanation_templates = [
            f"Multiple acute instability markers detected including {', '.join(critical_flags[:2])}. "
            f"Severity index reached {severity_index}, triggering emergency escalation protocol.",

            f"Clinical triage engine flagged {', '.join(critical_flags)}. "
            f"Aggregated physiological stress score ({score}) exceeds critical threshold requiring immediate care.",

            f"System identified life-threatening indicators such as {', '.join(critical_flags)}. "
            f"Immediate stabilization is necessary to prevent systemic deterioration."
        ]

        explanation = random.choice(explanation_templates)

    elif risk == "Moderate Attention":

        explanation_templates = [
            f"Combined contributing factors include {', '.join(reasoning[:3])}. "
            f"Severity index of {severity_index} indicates elevated but controlled clinical risk.",

            f"Observed physiological stressors such as {', '.join(reasoning[:2])}. "
            f"Urgent specialist review recommended to prevent escalation.",

            f"Risk score accumulation ({score}) suggests moderate instability driven by {', '.join(reasoning[:2])}."
        ]

        explanation = random.choice(explanation_templates)

    else:

        explanation_templates = [
            f"Clinical parameters remain within manageable deviation range. "
            f"Minor contributing elements include {', '.join(reasoning[:2]) if reasoning else 'isolated mild symptoms'}.",

            f"Severity index of {severity_index} indicates stable presentation. "
            f"No acute escalation markers detected.",

            f"Physiological readings show controlled risk profile with limited stress indicators."
        ]

        explanation = random.choice(explanation_templates)

    key_factors = critical_flags + reasoning

    return (
        risk,
        round(probability * 100, 2),   # Confidence %
        severity_index,               # 0-100 scale
        department,
        priority,
        wait_time,
        explanation,
        key_factors,
        factor_weights                # For graphs / AI weighting display
    )
