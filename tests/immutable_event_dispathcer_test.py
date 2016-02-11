from unittest import TestCase
from unittest.mock import Mock
from evee.event import Event
from evee.immutable_event_dispatcher import ImmutableEventDispatcher
from evee.event_dispatcher import EventDispatcher
from evee.exception import BadMethodCallError


class ImmutableEventDispatcherTest(TestCase):

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.__dispatcher = None
        self.__inner_dispatcher = None

    def setUp(self):
        self.__inner_dispatcher = EventDispatcher()
        self.__dispatcher = ImmutableEventDispatcher(self.__inner_dispatcher)

    def test_dispatch_delegates(self):
        event = Event()
        self.__inner_dispatcher.dispatch = Mock(return_value='result')
        self.assertEqual('result', self.__dispatcher.dispatch('event', event))
        self.__inner_dispatcher.dispatch.assert_called_with('event', event)

    def test_get_listeners_delegates(self):
        self.__inner_dispatcher.get_listeners = Mock(return_value='result')
        self.assertEqual('result', self.__dispatcher.get_listeners('event'))
        self.__inner_dispatcher.get_listeners.assert_called_with('event')

    def test_has_listeners_delegates(self):
        self.__inner_dispatcher.has_listeners = Mock(return_value='result')
        self.assertEqual('result', self.__dispatcher.has_listeners('event'))
        self.__inner_dispatcher.has_listeners.assert_called_with('event')

    def test_add_listener_disallowed(self):
        with self.assertRaises(BadMethodCallError):
            self.__dispatcher.add_listener('event', lambda event, name, dispatcher: event.stop_propagation())

    def test_add_subscriber_disallowed(self):
        with self.assertRaises(BadMethodCallError):
            subscriber = Mock()
            self.__dispatcher.add_subscriber(subscriber)

    def test_remove_listener_disallowed(self):
        with self.assertRaises(BadMethodCallError):
            self.__dispatcher.remove_listener('event', lambda event, name, dispatcher: event.stop_propagation())

    def test_remove_subscriber_disallowed(self):
        with self.assertRaises(BadMethodCallError):
            subscriber = Mock()
            self.__dispatcher.remove_subscriber(subscriber)
