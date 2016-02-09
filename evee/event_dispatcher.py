from evee.abstract_event_dispatcher import AbstractEventDispatcher
from typing import Callable
from typing import List
from typing import Sequence
from collections import OrderedDict
from evee.event import Event
from evee.abstract_event_subscriber import AbstractEventSubscriber


class EventDispatcher(AbstractEventDispatcher):
    def __init__(self):
        self.__listeners = {}
        self.__sorted = {}

    def dispatch(self, event_name: str, event: Event = None) -> Event:
        if not event:
            event = Event()

        listeners = self.get_listeners(event_name)
        if listeners:
            self._do_dispatch(listeners, event_name, event)

        return event

    def get_listeners(self, event_name: str = None) -> List:
        if event_name:
            if event_name not in self.__listeners:
                return {}
            if event_name not in self.__sorted:
                self.sort_listeners(event_name)

            return self.__sorted[event_name]

        for event_name, event_listener in self.__listeners.items():
            if event_name not in self.__sorted:
                self.sort_listeners(event_name)

        return dict([(key, value) for key, value in self.__sorted.items() if value != []])

    def get_listener_priority(self, event_name: str, listener: Callable) -> int:
        if event_name not in self.__listeners:
            return

        for priority, listeners in self.__listeners[event_name].items():
            try:
                listeners.index(listener)
                return priority
            except ValueError:
                pass

        return None

    def has_listeners(self, event_name: str = None) -> bool:
        return bool(len(self.get_listeners(event_name)))

    def add_listener(self, event_name: str = None, listener: Callable = None, priority: int = 0) -> object:
        if event_name not in self.__listeners:
            self.__listeners[event_name] = {}

        if priority not in self.__listeners[event_name]:
            self.__listeners[event_name][priority] = []

        self.__listeners[event_name][priority].append(listener)

        if event_name in self.__sorted:
            del self.__sorted[event_name]

    def remove_listener(self, event_name: str, listener: Callable):
        if event_name not in self.__listeners:
            return

        for priority, listeners in self.__listeners[event_name].items():
            try:
                key = listeners.index(listener)
                del self.__listeners[event_name][priority][key]
                if event_name in self.__sorted:
                    del self.__sorted[event_name]
            except ValueError:
                pass

    def add_subscriber(self, subscriber: AbstractEventSubscriber):
        for event_name, params in subscriber.get_subscribed_events().items():
            if isinstance(params, str):
                self.add_listener(event_name, getattr(subscriber, params))
            elif isinstance(params, list) and len(params) <= 2 and isinstance(params[0], str):
                priority = params[1] if len(params) > 1 else 0
                self.add_listener(event_name, getattr(subscriber, params[0]), priority)
            else:
                for listener in params:
                    priority = listener[1] if len(listener) > 1 else 0
                    self.add_listener(event_name, getattr(subscriber, listener[0]), priority)

    def remove_subscriber(self, subscriber: AbstractEventSubscriber):
        for event_name, params in subscriber.get_subscribed_events().items():
            if isinstance(params, list) and isinstance(params[0], list):
                for listener in params:
                    self.remove_listener(event_name, getattr(subscriber, listener[0]))
            else:
                parameters = params if isinstance(params, str) else params[0]
                self.remove_listener(event_name, getattr(subscriber, parameters))

    def _do_dispatch(self, listeners: Sequence[Callable[[Event, str, AbstractEventDispatcher], Event]],
                     event_name: str, event: Event):
        """
        Triggers the listeners of an event. This method can be overridden
        to add functionality that is executed for each listener.

        :param listeners:  List of event listeners
        :param event_name: The name of the event to dispatch
        :param event:      The event obbject to pass to the event handlers/listeners
        """
        for listener in listeners:
            listener(event, event_name, self)
            if event.is_propagation_stopped():
                break

    def sort_listeners(self, event_name: str):
        """
        Sorts the internal list of listeners for the given event by priority.

        :param event_name: the name of the event
        """
        listeners = OrderedDict(sorted(self.__listeners[event_name].items(), reverse=True))
        ordered_listeners = []

        for priority, listener in listeners.items():
            ordered_listeners += listener

        self.__sorted[event_name] = ordered_listeners
