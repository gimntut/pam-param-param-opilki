from dataclasses import dataclass

from utils.event_bus import BaseEvent


@dataclass
class ProductsUpdateEvent(BaseEvent):
    count: int = 0


@dataclass
class ProductsCreateEvent(BaseEvent):
    count: int = 0
