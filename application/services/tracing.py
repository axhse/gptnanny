from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, List, Dict


class Event:
    def __init__(self, name: str, event_info: Any = None):
        self.__name: str = name
        self.__info: Any = event_info
        self.__time: datetime = datetime.utcnow()

    @property
    def name(self) -> str:
        return self.__name

    @property
    def info(self) -> Any:
        return self.__info

    @property
    def time(self) -> datetime:
        return self.__time


class Trace:
    def __init__(self):
        self.__events: List[Event] = list()
        # TODO: uid

    @property
    def count(self) -> int:
        return len(self.__events)

    def add(self, event: Event) -> None:
        self.__events.append(event)

    def json(self) -> List[Dict]:
        return [
            {
                "name": event.name,
                "info": event.info,
                "time": event.time.isoformat(),
            }
            for event in self.__events
        ]


class Tracing(ABC):
    def __init__(self):
        self.__all_trace: List[Trace] = list()

    def create(self) -> Trace:
        trace = Trace()
        self.__all_trace.append(trace)
        return trace

    @abstractmethod
    def save_all(self) -> None:
        pass


class MockTracing(Tracing):
    def save_all(self) -> None:
        pass
