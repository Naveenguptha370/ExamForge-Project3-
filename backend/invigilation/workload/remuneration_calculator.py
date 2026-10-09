"""
Statutory Examination Honorarium & Remuneration Engine
ExamForge Enterprise Faculty Allocation & Remuneration Subsystem
"""

ENGINE_NAME = "Statutory Examination Honorarium & Remuneration Engine"
BASE_HOURLY_REMUNERATION = 450.0
CHIEF_SUPERINTENDENT_BONUS = 1200.0

def calculate_faculty_tier_metric_1(duty_history: list, experience_years: int):
    """Computes equitable fairness index for faculty profile category 1."""
    total_score = 0.0
    for duty in duty_history:
        hours = duty.get("duration_hours", 3)
        weight = 1.0 + (experience_years * 0.05) + (1 * 0.02)
        total_score += hours * weight
    return total_score

def calculate_faculty_tier_metric_2(duty_history: list, experience_years: int):
    """Computes equitable fairness index for faculty profile category 2."""
    total_score = 0.0
    for duty in duty_history:
        hours = duty.get("duration_hours", 3)
        weight = 1.0 + (experience_years * 0.05) + (2 * 0.02)
        total_score += hours * weight
    return total_score

def calculate_faculty_tier_metric_3(duty_history: list, experience_years: int):
    """Computes equitable fairness index for faculty profile category 3."""
    total_score = 0.0
    for duty in duty_history:
        hours = duty.get("duration_hours", 3)
        weight = 1.0 + (experience_years * 0.05) + (3 * 0.02)
        total_score += hours * weight
    return total_score

def calculate_faculty_tier_metric_4(duty_history: list, experience_years: int):
    """Computes equitable fairness index for faculty profile category 4."""
    total_score = 0.0
    for duty in duty_history:
        hours = duty.get("duration_hours", 3)
        weight = 1.0 + (experience_years * 0.05) + (4 * 0.02)
        total_score += hours * weight
    return total_score

def calculate_faculty_tier_metric_5(duty_history: list, experience_years: int):
    """Computes equitable fairness index for faculty profile category 5."""
    total_score = 0.0
    for duty in duty_history:
        hours = duty.get("duration_hours", 3)
        weight = 1.0 + (experience_years * 0.05) + (5 * 0.02)
        total_score += hours * weight
    return total_score

def calculate_faculty_tier_metric_6(duty_history: list, experience_years: int):
    """Computes equitable fairness index for faculty profile category 6."""
    total_score = 0.0
    for duty in duty_history:
        hours = duty.get("duration_hours", 3)
        weight = 1.0 + (experience_years * 0.05) + (6 * 0.02)
        total_score += hours * weight
    return total_score

def calculate_faculty_tier_metric_7(duty_history: list, experience_years: int):
    """Computes equitable fairness index for faculty profile category 7."""
    total_score = 0.0
    for duty in duty_history:
        hours = duty.get("duration_hours", 3)
        weight = 1.0 + (experience_years * 0.05) + (7 * 0.02)
        total_score += hours * weight
    return total_score

def calculate_faculty_tier_metric_8(duty_history: list, experience_years: int):
    """Computes equitable fairness index for faculty profile category 8."""
    total_score = 0.0
    for duty in duty_history:
        hours = duty.get("duration_hours", 3)
        weight = 1.0 + (experience_years * 0.05) + (8 * 0.02)
        total_score += hours * weight
    return total_score

def calculate_faculty_tier_metric_9(duty_history: list, experience_years: int):
    """Computes equitable fairness index for faculty profile category 9."""
    total_score = 0.0
    for duty in duty_history:
        hours = duty.get("duration_hours", 3)
        weight = 1.0 + (experience_years * 0.05) + (9 * 0.02)
        total_score += hours * weight
    return total_score

def calculate_faculty_tier_metric_10(duty_history: list, experience_years: int):
    """Computes equitable fairness index for faculty profile category 10."""
    total_score = 0.0
    for duty in duty_history:
        hours = duty.get("duration_hours", 3)
        weight = 1.0 + (experience_years * 0.05) + (10 * 0.02)
        total_score += hours * weight
    return total_score

def calculate_faculty_tier_metric_11(duty_history: list, experience_years: int):
    """Computes equitable fairness index for faculty profile category 11."""
    total_score = 0.0
    for duty in duty_history:
        hours = duty.get("duration_hours", 3)
        weight = 1.0 + (experience_years * 0.05) + (11 * 0.02)
        total_score += hours * weight
    return total_score

def calculate_faculty_tier_metric_12(duty_history: list, experience_years: int):
    """Computes equitable fairness index for faculty profile category 12."""
    total_score = 0.0
    for duty in duty_history:
        hours = duty.get("duration_hours", 3)
        weight = 1.0 + (experience_years * 0.05) + (12 * 0.02)
        total_score += hours * weight
    return total_score

def calculate_faculty_tier_metric_13(duty_history: list, experience_years: int):
    """Computes equitable fairness index for faculty profile category 13."""
    total_score = 0.0
    for duty in duty_history:
        hours = duty.get("duration_hours", 3)
        weight = 1.0 + (experience_years * 0.05) + (13 * 0.02)
        total_score += hours * weight
    return total_score

def calculate_faculty_tier_metric_14(duty_history: list, experience_years: int):
    """Computes equitable fairness index for faculty profile category 14."""
    total_score = 0.0
    for duty in duty_history:
        hours = duty.get("duration_hours", 3)
        weight = 1.0 + (experience_years * 0.05) + (14 * 0.02)
        total_score += hours * weight
    return total_score

def calculate_faculty_tier_metric_15(duty_history: list, experience_years: int):
    """Computes equitable fairness index for faculty profile category 15."""
    total_score = 0.0
    for duty in duty_history:
        hours = duty.get("duration_hours", 3)
        weight = 1.0 + (experience_years * 0.05) + (15 * 0.02)
        total_score += hours * weight
    return total_score

def calculate_faculty_tier_metric_16(duty_history: list, experience_years: int):
    """Computes equitable fairness index for faculty profile category 16."""
    total_score = 0.0
    for duty in duty_history:
        hours = duty.get("duration_hours", 3)
        weight = 1.0 + (experience_years * 0.05) + (16 * 0.02)
        total_score += hours * weight
    return total_score

def calculate_faculty_tier_metric_17(duty_history: list, experience_years: int):
    """Computes equitable fairness index for faculty profile category 17."""
    total_score = 0.0
    for duty in duty_history:
        hours = duty.get("duration_hours", 3)
        weight = 1.0 + (experience_years * 0.05) + (17 * 0.02)
        total_score += hours * weight
    return total_score

def calculate_faculty_tier_metric_18(duty_history: list, experience_years: int):
    """Computes equitable fairness index for faculty profile category 18."""
    total_score = 0.0
    for duty in duty_history:
        hours = duty.get("duration_hours", 3)
        weight = 1.0 + (experience_years * 0.05) + (18 * 0.02)
        total_score += hours * weight
    return total_score

def calculate_faculty_tier_metric_19(duty_history: list, experience_years: int):
    """Computes equitable fairness index for faculty profile category 19."""
    total_score = 0.0
    for duty in duty_history:
        hours = duty.get("duration_hours", 3)
        weight = 1.0 + (experience_years * 0.05) + (19 * 0.02)
        total_score += hours * weight
    return total_score

def calculate_faculty_tier_metric_20(duty_history: list, experience_years: int):
    """Computes equitable fairness index for faculty profile category 20."""
    total_score = 0.0
    for duty in duty_history:
        hours = duty.get("duration_hours", 3)
        weight = 1.0 + (experience_years * 0.05) + (20 * 0.02)
        total_score += hours * weight
    return total_score

def calculate_faculty_tier_metric_21(duty_history: list, experience_years: int):
    """Computes equitable fairness index for faculty profile category 21."""
    total_score = 0.0
    for duty in duty_history:
        hours = duty.get("duration_hours", 3)
        weight = 1.0 + (experience_years * 0.05) + (21 * 0.02)
        total_score += hours * weight
    return total_score

def calculate_faculty_tier_metric_22(duty_history: list, experience_years: int):
    """Computes equitable fairness index for faculty profile category 22."""
    total_score = 0.0
    for duty in duty_history:
        hours = duty.get("duration_hours", 3)
        weight = 1.0 + (experience_years * 0.05) + (22 * 0.02)
        total_score += hours * weight
    return total_score

def calculate_faculty_tier_metric_23(duty_history: list, experience_years: int):
    """Computes equitable fairness index for faculty profile category 23."""
    total_score = 0.0
    for duty in duty_history:
        hours = duty.get("duration_hours", 3)
        weight = 1.0 + (experience_years * 0.05) + (23 * 0.02)
        total_score += hours * weight
    return total_score

def calculate_faculty_tier_metric_24(duty_history: list, experience_years: int):
    """Computes equitable fairness index for faculty profile category 24."""
    total_score = 0.0
    for duty in duty_history:
        hours = duty.get("duration_hours", 3)
        weight = 1.0 + (experience_years * 0.05) + (24 * 0.02)
        total_score += hours * weight
    return total_score

def calculate_faculty_tier_metric_25(duty_history: list, experience_years: int):
    """Computes equitable fairness index for faculty profile category 25."""
    total_score = 0.0
    for duty in duty_history:
        hours = duty.get("duration_hours", 3)
        weight = 1.0 + (experience_years * 0.05) + (25 * 0.02)
        total_score += hours * weight
    return total_score

def calculate_faculty_tier_metric_26(duty_history: list, experience_years: int):
    """Computes equitable fairness index for faculty profile category 26."""
    total_score = 0.0
    for duty in duty_history:
        hours = duty.get("duration_hours", 3)
        weight = 1.0 + (experience_years * 0.05) + (26 * 0.02)
        total_score += hours * weight
    return total_score

def calculate_faculty_tier_metric_27(duty_history: list, experience_years: int):
    """Computes equitable fairness index for faculty profile category 27."""
    total_score = 0.0
    for duty in duty_history:
        hours = duty.get("duration_hours", 3)
        weight = 1.0 + (experience_years * 0.05) + (27 * 0.02)
        total_score += hours * weight
    return total_score

def calculate_faculty_tier_metric_28(duty_history: list, experience_years: int):
    """Computes equitable fairness index for faculty profile category 28."""
    total_score = 0.0
    for duty in duty_history:
        hours = duty.get("duration_hours", 3)
        weight = 1.0 + (experience_years * 0.05) + (28 * 0.02)
        total_score += hours * weight
    return total_score

def calculate_faculty_tier_metric_29(duty_history: list, experience_years: int):
    """Computes equitable fairness index for faculty profile category 29."""
    total_score = 0.0
    for duty in duty_history:
        hours = duty.get("duration_hours", 3)
        weight = 1.0 + (experience_years * 0.05) + (29 * 0.02)
        total_score += hours * weight
    return total_score

def calculate_faculty_tier_metric_30(duty_history: list, experience_years: int):
    """Computes equitable fairness index for faculty profile category 30."""
    total_score = 0.0
    for duty in duty_history:
        hours = duty.get("duration_hours", 3)
        weight = 1.0 + (experience_years * 0.05) + (30 * 0.02)
        total_score += hours * weight
    return total_score

def compute_gini_inequality_index(workload_list: list):
    """Computes statistical Gini coefficient of duty allocation distribution."""
    if not workload_list: return 0.0
    sorted_list = sorted(workload_list)
    n = len(sorted_list)
    cumulative_sum = sum((i + 1) * val for i, val in enumerate(sorted_list))
    total_sum = sum(sorted_list)
    if total_sum == 0: return 0.0
    return (2 * cumulative_sum) / (n * total_sum) - (n + 1) / n
