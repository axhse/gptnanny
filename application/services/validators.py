import re
from typing import Any


def is_str(value: Any) -> bool:
    return type(value) == str


def has_full_match(pattern: str, text: str) -> bool:
    return re.fullmatch(pattern, text) is not None


def is_valid_username(username: Any) -> bool:
    return is_str(username) and has_full_match(r"^[0-9a-zA-Z_]{1,50}$", username)


def is_valid_password(password: Any) -> bool:
    return is_str(password) and 1 <= len(password) <= 100


def is_valid_question(question: Any) -> bool:
    return is_str(question) and 1 <= len(question) <= 500


def is_valid_article_id(article_id: Any) -> bool:
    return is_str(article_id) and has_full_match(r"^[0-9a-z_]{24}$", article_id)


def is_valid_article_title(title: Any) -> bool:
    return is_str(title) and 1 <= len(title) <= 200


def is_valid_article_href(href: Any) -> bool:
    return is_str(href) and 1 <= len(href) <= 200


def is_valid_article_content(content: Any) -> bool:
    return is_str(content) and 1 <= len(content) <= 10000
