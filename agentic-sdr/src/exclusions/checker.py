from rapidfuzz import process, fuzz
from src.exclusions.lists import CUSTOMERS, STRATEGIC, TARGET

FUZZY_THRESHOLD = 88  # score out of 100


def _check_list(name: str, lst: list[str]) -> str | None:
    result = process.extractOne(name, lst, scorer=fuzz.token_set_ratio)
    if result and result[1] >= FUZZY_THRESHOLD:
        return result[0]
    return None


def check_exclusion(company_name: str) -> dict:
    """
    Returns {"excluded": bool, "reason": str | None, "matched": str | None}
    """
    name = company_name.strip()

    match = _check_list(name, CUSTOMERS)
    if match:
        return {"excluded": True, "reason": "customer", "matched": match}

    match = _check_list(name, STRATEGIC)
    if match:
        return {"excluded": True, "reason": "strategic", "matched": match}

    match = _check_list(name, TARGET)
    if match:
        return {"excluded": True, "reason": "target", "matched": match}

    return {"excluded": False, "reason": None, "matched": None}
