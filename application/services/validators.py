import re
from typing import Optional


def is_valid_question(question: Optional[str]) -> bool:
    return question is not None and 1 <= len(question) <= 500


def is_valid_article_id(article_id: Optional[str]) -> bool:
    if article_id is None:
        return False
    return re.fullmatch(r"^[0-9a-z_]{24}$", article_id) is not None


def is_valid_article_title(title: Optional[str]) -> bool:
    return title is not None and 1 <= len(title) <= 200


def is_valid_article_href(href: Optional[str]) -> bool:
    return href is not None and 1 <= len(href) <= 200


def is_valid_article_content(content: Optional[str]) -> bool:
    return content is not None and 1 <= len(content) <= 10000
