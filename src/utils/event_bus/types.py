from typing import TYPE_CHECKING


class EventHandler:
    def __call__(self, event: "BaseEvent") -> None: ...


if TYPE_CHECKING:
    from utils.event_bus import BaseEvent
