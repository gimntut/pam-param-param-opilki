from dataclasses import dataclass
from typing import Type

from utils.event_bus.types import EventHandler


@dataclass
class Subscribe:
    event_class: Type["BaseEvent"]
    handler: EventHandler

    def enable(self) -> None:
        self.event_class.register(self.handler)

    def disable(self) -> None:
        self.event_class.register(self.handler)


class BaseEvent:
    _handlers: set[EventHandler]

    @classmethod
    def register(cls, handler: EventHandler) -> Subscribe:
        assert cls is not BaseEvent, "Класс события должен наследоваться от BaseEvent"
        if not hasattr(cls, "_handlers"):
            cls._handlers = set()
        cls._handlers.add(handler)
        return Subscribe(event_class=cls, handler=handler)

    @classmethod
    def unregister(cls, handler: EventHandler) -> None:
        if not hasattr(cls, "_handlers"):
            cls._handlers = set()
        cls._handlers.remove(handler)

    @classmethod
    def do(cls, event: "BaseEvent") -> None:
        for handler in getattr(cls, "_handlers", []):
            handler(event)


class EventBus:
    def __init__(self):
        self._queue = []

    def push(self, event: BaseEvent):
        self._queue.append(event)

    def publish(self, classes=None):
        new_queue = []
        default_doing = classes is None
        classes = classes or ()
        for event in self._queue:
            doing = default_doing
            for cls in type(event).mro():
                doing = doing or cls in classes
                if doing and issubclass(cls, BaseEvent) and cls != BaseEvent:
                    cls.do(event)
            if not doing:
                new_queue.append(event)
        self._queue = new_queue


event_bus = EventBus()
