from dataclasses import dataclass
from typing import Any

@dataclass
class DomainEvent:
    pass

@dataclass
class AppointmentCreated(DomainEvent):
    appointment: Any

@dataclass
class AppointmentUpdated(DomainEvent):
    appointment: Any

@dataclass
class AppointmentDeleted(DomainEvent):
    appointment: Any

class DomainEventPublisher:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def publish(self, event: DomainEvent):
        for subscriber in self.subscribers:
            subscriber.handle(event)
