import logging
import secrets
from abc import ABC, abstractmethod
from random import random
from time import sleep
from typing import List, Optional

from xata import XataClient

from application.services.data_helpers import resp_to_str

LOGGER = logging.getLogger(__name__)


class Article:
    def __init__(
        self, article_id: str = "", title: str = "", href: str = "", content: str = ""
    ):
        self.id: str = article_id
        self.title: str = title
        self.href: str = href
        self.content: str = content

    def json(self):
        return {
            "id": self.id,
            "title": self.title,
            "href": self.href,
            "content": self.content,
        }


class Answer:
    def __init__(self, message: str, articles: List[Article]):
        self.message: str = message
        self.articles: List[Article] = articles

    def json(self):
        return {"message": self.message, "articles": [s.json() for s in self.articles]}


class Consultant(ABC):
    @abstractmethod
    def ask(self, question: str) -> Optional[Answer]:
        pass

    @abstractmethod
    def get_article(
        self, article_id: str, with_content: bool = False
    ) -> Optional[Article]:
        pass

    @abstractmethod
    def get_articles_short(self) -> Optional[List[Article]]:
        pass

    @abstractmethod
    def create_article(self, article: Article) -> Optional[str]:
        pass

    @abstractmethod
    def update_article(self, article: Article) -> bool:
        pass

    @abstractmethod
    def delete_article(self, article_id: str) -> bool:
        pass


class MockConsultant(Consultant):
    def __init__(self):
        self._articles: List[Article] = [
            Article(
                secrets.token_hex(24 // 2), "First Title", "first href", "First Text"
            ),
            Article(
                secrets.token_hex(24 // 2), "Second Title", "second href", "Second Text"
            ),
        ]

    def ask(self, question: str) -> Optional[Answer]:
        sleep(1 + random() * 3)
        if question.lower() in ["error", "null", "none"]:
            return None
        article = Article(title="Google", href="https://google.com")
        answer = Answer("The answer will be here.", [article])
        return answer

    def get_article(
        self, article_id: str, with_content: bool = False
    ) -> Optional[Article]:
        sleep(0.5 + random() * 1)
        for article in self._articles:
            if article.id == article_id:
                return article
        return None

    def get_articles_short(self) -> Optional[List[Article]]:
        sleep(0.5 + random() * 1.5)
        articles = list()
        for article in self._articles:
            articles.append(Article(article.id, article.title, article.href))
        return articles

    def create_article(self, article: Article) -> Optional[str]:
        sleep(0.5 + random() * 1)
        article.id = secrets.token_hex(24 // 2)
        self._articles.append(article)
        return article.id

    def update_article(self, article: Article) -> bool:
        sleep(0.5 + random() * 1.5)
        for index in range(len(self._articles) - 1, -1, -1):
            if self._articles[index].id == article.id:
                self._articles.pop(index)
                self._articles.append(article)
                return True
        return False

    def delete_article(self, article_id: str) -> bool:
        sleep(0.5 + random() * 1)
        for index in range(len(self._articles) - 1, -1, -1):
            if self._articles[index].id == article_id:
                self._articles.pop(index)
        return True


class XataConsultant(Consultant):
    WORKSPACE_ID = "77mmm6"
    REGION = "eu-central-1"
    DB_NAME = "gptnanny"
    TABLE_NAME = "article"
    BRANCH_NAME = "main"

    def __init__(self, api_key: str):
        self.__client: XataClient = XataClient(
            api_key=api_key,
            workspace_id=self.WORKSPACE_ID,
            region=self.REGION,
            db_name=self.DB_NAME,
            branch_name=self.BRANCH_NAME,
        )

    def ask(self, question) -> Optional[Answer]:
        try:
            payload = {"question": question}
            resp = self.__client.search_and_filter().askTable(self.TABLE_NAME, payload)
            LOGGER.debug(resp_to_str(resp))
            if resp.status_code != 200:
                return None
            answer = Answer(resp.json()["answer"], list())
            article_ids = resp.json()["records"][:1]
            for article_id in article_ids:
                article = self.get_article(article_id)
                if article is None:
                    return None
                article.id = ""
                article.content = ""
                answer.articles.append(article)
            return answer
        except Exception as error:
            LOGGER.error(error)
            return None

    def get_article(
        self, article_id: str, with_content: bool = False
    ) -> Optional[Article]:
        try:
            columns = ["id", "title", "href"]
            if with_content:
                columns.append("content")
            resp = self.__client.records().getRecord(
                self.TABLE_NAME, article_id, columns=columns
            )
            LOGGER.debug(resp_to_str(resp))
            if resp.status_code != 200:
                return None
            props = resp.json()
            content = props.get("content", "")
            return Article(props["id"], props["title"], props["href"], content)
        except Exception as error:
            LOGGER.error(error)
            return None

    def get_articles_short(self) -> Optional[List[Article]]:
        columns = [
            {"name": "id", "type": "string"},
            {"name": "title", "type": "string"},
            {"name": "href", "type": "string"},
        ]
        payload = {
            "columns": columns,
        }
        resp = self.__client.data().queryTable(self.TABLE_NAME, payload)
        LOGGER.debug(resp_to_str(resp))
        if resp.status_code != 200:
            return None
        records = list()
        for data in resp.json()["records"]:
            records.append(Article(data["id"], data["title"], data["href"]))
        return records

    def create_article(self, article: Article) -> Optional[str]:
        try:
            data = article.json()
            data.pop("id")
            resp = self.__client.records().insertRecord(self.TABLE_NAME, data)
            LOGGER.debug(resp_to_str(resp))
            if resp.status_code != 201:
                return None
            return resp.json()["id"]
        except Exception as error:
            LOGGER.error(error)
            return None

    def update_article(self, article: Article) -> bool:
        try:
            data = article.json()
            data.pop("id")
            resp = self.__client.records().updateRecordWithID(
                self.TABLE_NAME, article.id, data
            )
            LOGGER.debug(resp_to_str(resp))
            return resp.status_code == 200
        except Exception as error:
            LOGGER.error(error)
            return False

    def delete_article(self, article_id: str) -> bool:
        try:
            resp = self.__client.records().deleteRecord(self.TABLE_NAME, article_id)
            LOGGER.debug(resp_to_str(resp))
            return resp.status_code == 204
        except Exception as error:
            LOGGER.error(error)
            return False
