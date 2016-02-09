from tests.abstract_event_dispatcher_test import AbstractEventDispatcherTest
from evee.event_dispatcher import EventDispatcher


class EventDispatcherTest(AbstractEventDispatcherTest):
    def create_event_dispatcher(self):
        return EventDispatcher()

    def test_initial_state(self):
        self._initial_state()

    def test_add_listener(self):
        self._add_listener()

    def test_get_listeners_sorts_by_priority(self):
        self._get_listeners_sorts_by_priority()

    def test_get_all_listeners_sorts_by_priority(self):
        self._get_all_listeners_sorts_by_priority()

    def test_get_listener_priority(self):
        self._get_listener_priority()

    def test_dispatch(self):
        self._dispatch()

    def test_dispatch_for_lambda(self):
        self._dispatch_for_lambda()

    def test_stop_event_propagation(self):
        self._stop_event_propagation()

    def test_dispatch_by_priority(self):
        self._dispatch_by_priority()

    def test_remove_listener(self):
        self._remove_listener()

    def test_add_subscriber(self):
        self._add_subscriber()

    def test_add_subscriber_with_priorities(self):
        self._add_subscriber_with_priorities()

    def test_add_subscriber_with_multiple_listeners(self):
        self._add_subscriber_with_multiple_listeners()

    def test_remove_subscriber(self):
        self._remove_subscriber()

    def test_remove_subscriber_with_priorities(self):
        self._remove_subscriber_with_priorities()

    def test_remove_subscriber_with_multiple_listeners(self):
        self._remove_subscriber_with_multiple_listeners()

    def test_event_receives_the_dispatcher_instance_as_argument(self):
        self._event_receives_the_dispatcher_instance_as_argument()

    def test_has_listeners_when_added_callback_listener_is_removed(self):
        self._has_listeners_when_added_callback_listener_is_removed()

    def test_get_listeners_when_added_callback_listener_is_removed(self):
        self._get_listeners_when_added_callback_listener_is_removed()

    def test_has_listeners_without_events_returns_false_after_has_listeners_with_event_has_been_called(self):
        self._has_listeners_without_events_returns_false_after_has_listeners_with_event_has_been_called()
