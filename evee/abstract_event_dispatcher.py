#
# This file is part of the onema.io evee Package.
# For the full copyright and license information,
# please view the LICENSE file that was distributed
# with this source code.
#
# @author Juan Manuel Torres <software@onema.io>
#
from abc import abstractmethod, ABC
from typing import Callable, Any, Optional, Sequence

from evee.abstract_event_subscriber import AbstractEventSubscriber
from evee.event import Event


class AbstractEventDispatcher(ABC):

    @abstractmethod
    def dispatch(self, event_name: str, event: Event = None) -> Event:
        """
        Dispatches an event to all registered listeners.

        :param event_name: The name of the event to dispatch. The name of the event
                            is the name of the method that is invoked on listeners
        :param event:      The event to pass to the event handlers/listeners
                            If not supplied, an empty Event instance is created
        :return:           An instance of Event
        """

    @abstractmethod
    def add_listener(self, event_name: str, listener: Callable = None, priority: int = 0):
        """
        Adds an event listener that listens on the specified events.

        :param event_name: The event to listen on
        :param listener:   The listener
        :param priority:   The higher this value, the earlier an event listener
                            will be triggered in the chain (defaults to 0)
        """

    @abstractmethod
    def add_subscriber(self, subscriber: AbstractEventSubscriber):
        """
        Adds an event subscriber. The subscriber is asked for all the events he is
        interested in and added as a listener for these events.

        :param subscriber:  The subscriber
        """

    @abstractmethod
    def remove_listener(self, event_name: str, listener: Callable):
        """
        Removes an event listener from the specified events.

        :param event_name: The event to remove a listener from
        :param listener:   The listener to remove
        """

    @abstractmethod
    def remove_subscriber(self, subscriber: AbstractEventSubscriber):
        """
        Removes an event subscriber.

        :param subscriber: The subscriber
        :return:
        """

    @abstractmethod
    def get_listeners(self, event_name: str = None) -> Sequence[Callable[[Event, str, Any], Event]]:
        """
        Gets the listener of a specific event or all listeners stored by
        descending priority.

        :param event_name: The name of the event
        :return:           The event listeners for the specified event, or all
                            event listeners by event name
        """

    @abstractmethod
    def get_listener_priority(self, event_name: str, listener: Callable) -> Optional[Any]:
        """
        Get the listener priority for a specific event.

        :param event_name: The name of the event
        :param listener:   The listener
        :return:           The event listener priority
        """

    @abstractmethod
    def has_listeners(self, event_name: str = None) -> bool:
        """
        Check if the listener exist.

        :param event_name: The name of the event
        """
