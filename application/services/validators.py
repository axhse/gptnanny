from typing import Optional


def is_valid_question(question: Optional[str]) -> bool:
    return question is not None and 1 <= len(question) <= 500
