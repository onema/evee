from abc import ABCMeta
from abc import abstractmethod
from unittest import TestCase
from evee import Event
from evee import AbstractEventSubscriber


class AbstractEventDispatcherTest(TestCase, metaclass=ABCMeta):

    PRE_FOO = 'pre.foo'
    POST_FOO = 'post.foo'
    PRE_BAR = 'pre.bar'
    POST_BAR = 'post.bar'

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.__dispatcher = None
        self.__listener = None

    def setUp(self):
        self.__dispatcher = self.create_event_dispatcher()
        self.__listener = TestEventListener()

    @abstractmethod
    def create_event_dispatcher(self):
        pass

    def _initial_state(self):
        self.assertEqual({}, self.__dispatcher.get_listeners())
        self.assertFalse(self.__dispatcher.has_listeners(self.PRE_FOO))
        self.assertFalse(self.__dispatcher.has_listeners(self.POST_FOO))

    def _add_listener(self):
        self.__dispatcher.add_listener('pre.foo', getattr(self.__listener, 'pre_foo'))
        self.__dispatcher.add_listener('post.foo', getattr(self.__listener, 'post_foo'))
        self.assertTrue(self.__dispatcher.has_listeners(self.PRE_FOO))
        self.assertEqual(1, len(self.__dispatcher.get_listeners(self.PRE_FOO)))
        self.assertEqual(1, len(self.__dispatcher.get_listeners(self.POST_FOO)))
        self.assertEqual(2, len(self.__dispatcher.get_listeners()))

    def _get_listeners_sorts_by_priority(self):
        listener_1 = TestEventListener()
        listener_2 = TestEventListener()
        listener_3 = TestEventListener()
        listener_1.name = '1'
        listener_2.name = '2'
        listener_3.name = '3'

        self.__dispatcher.add_listener('pre.foo', getattr(listener_1, 'pre_foo'), -10)
        self.__dispatcher.add_listener('pre.foo', getattr(listener_2, 'pre_foo'), 10)
        self.__dispatcher.add_listener('pre.foo', getattr(listener_3, 'pre_foo'))

        expected = [
            getattr(listener_2, 'pre_foo'),
            getattr(listener_3, 'pre_foo'),
            getattr(listener_1, 'pre_foo')
        ]

        self.assertListEqual(expected, self.__dispatcher.get_listeners('pre.foo'))

    def _get_all_listeners_sorts_by_priority(self):
        listener_1 = TestEventListener()
        listener_2 = TestEventListener()
        listener_3 = TestEventListener()
        listener_4 = TestEventListener()
        listener_5 = TestEventListener()
        listener_6 = TestEventListener()

        self.__dispatcher.add_listener('pre.foo', listener_1, -10)
        self.__dispatcher.add_listener('pre.foo', listener_2)
        self.__dispatcher.add_listener('pre.foo', listener_3, 10)
        self.__dispatcher.add_listener('post.foo', listener_4, -10)
        self.__dispatcher.add_listener('post.foo', listener_5)
        self.__dispatcher.add_listener('post.foo', listener_6, 10)

        expected = {
            'pre.foo': [listener_3, listener_2, listener_1],
            'post.foo': [listener_6, listener_5, listener_4],
        }

        self.assertDictEqual(expected, self.__dispatcher.get_listeners())

    def _get_listener_priority(self):
        listener_1 = TestEventListener()
        listener_2 = TestEventListener()

        self.__dispatcher.add_listener('pre.foo', listener_1, -10)
        self.__dispatcher.add_listener('pre.foo', listener_2)

        self.assertEqual(-10, self.__dispatcher.get_listener_priority('pre.foo', listener_1))
        self.assertEqual(0, self.__dispatcher.get_listener_priority('pre.foo', listener_2))
        self.assertIsNone(self.__dispatcher.get_listener_priority('pre.bar', listener_2))

    def _dispatch(self):
        self.__dispatcher.add_listener('pre.foo', getattr(self.__listener, 'pre_foo'))
        self.__dispatcher.add_listener('post.foo', getattr(self.__listener, 'post_foo'))
        self.__dispatcher.dispatch(self.PRE_FOO)

        self.assertTrue(self.__listener.pre_foo_invoked)
        self.assertFalse(self.__listener.post_foo_invoked)
        self.assertIsInstance(self.__dispatcher.dispatch('noevent'), Event)
        self.assertIsInstance(self.__dispatcher.dispatch(self.PRE_FOO), Event)
        event = Event()
        return_value = self.__dispatcher.dispatch(self.PRE_FOO, event)
        self.assertEqual(event, return_value)

    def _dispatch_for_lambda(self):
        listener = lambda event, name, dispatcher: event.invoke()
        event = TestEvent()
        self.__dispatcher.add_listener('pre.foo', listener)
        self.__dispatcher.add_listener('post.foo', listener)
        self.__dispatcher.dispatch(self.PRE_FOO, event)
        self.assertEqual(1, event.times_invoked)

    def _dispatch_for_function(self):
        def listener(event, name, dispatcher):
            event.invoke()
        event = TestEvent()
        self.__dispatcher.add_listener('pre.foo', listener)
        self.__dispatcher.add_listener('post.foo', listener)
        self.__dispatcher.dispatch(self.POST_FOO, event)
        self.assertEqual(1, event.times_invoked)

    def _stop_event_propagation(self):
        other_listener = TestEventListener()

        self.__dispatcher.add_listener('post.foo', getattr(self.__listener, 'post_foo'), 10)
        self.__dispatcher.add_listener('post.foo', getattr(other_listener,'pre_foo'))
        self.__dispatcher.dispatch(self.POST_FOO)
        self.assertTrue(self.__listener.post_foo_invoked)
        self.assertFalse(other_listener.post_foo_invoked)

    def _dispatch_by_priority(self):
        invoked = []
        listener1 = lambda event, name, dispatcher: invoked.append('1')
        listener2 = lambda event, name, dispatcher: invoked.append('2')
        listener3 = lambda event, name, dispatcher: invoked.append('3')

        self.__dispatcher.add_listener('pre.foo', listener1, -10)
        self.__dispatcher.add_listener('pre.foo', listener2)
        self.__dispatcher.add_listener('pre.foo', listener3, 10)
        self.__dispatcher.dispatch(self.PRE_FOO)
        self.assertListEqual(['3', '2', '1'], invoked)

    def _remove_listener(self):
        self.__dispatcher.add_listener('pre.bar', self.__listener)
        self.assertTrue(self.__dispatcher.has_listeners(self.PRE_BAR))
        self.__dispatcher.remove_listener('pre.bar', self.__listener)
        self.assertFalse(self.__dispatcher.has_listeners(self.PRE_BAR))
        self.__dispatcher.remove_listener('notExist', self.__listener)

    def _add_subscriber(self):
        event_subscriber = TestEventSubscriber()
        self.__dispatcher.add_subscriber(event_subscriber)
        self.assertTrue(self.__dispatcher.has_listeners(self.PRE_FOO))
        self.assertTrue(self.__dispatcher.has_listeners(self.POST_FOO))

    def _add_subscriber_with_priorities(self):
        event_subscriber = TestEventSubscriber()
        self.__dispatcher.add_subscriber(event_subscriber)

        event_subscriber = TestEventSubscriberWithPriorities()
        self.__dispatcher.add_subscriber(event_subscriber)

        listeners = self.__dispatcher.get_listeners('pre.foo')
        self.assertTrue(self.__dispatcher.has_listeners(self.PRE_FOO))
        self.assertEqual(2, len(listeners))
        self.assertEqual(getattr(event_subscriber, 'pre_foo1'), listeners[0])

    def _add_subscriber_with_multiple_listeners(self):
        event_subscriber = TestEventSubscriberWithMultipleListeners()
        self.__dispatcher.add_subscriber(event_subscriber)

        listeners = self.__dispatcher.get_listeners('pre.foo')
        self.assertTrue(self.__dispatcher.has_listeners(self.PRE_FOO))
        self.assertEqual(2, len(listeners))
        self.assertEqual(getattr(event_subscriber, 'pre_foo2'), listeners[0])

    def _remove_subscriber(self):
        event_subscriber = TestEventSubscriber()
        self.__dispatcher.add_subscriber(event_subscriber)
        self.assertTrue(self.__dispatcher.has_listeners(self.PRE_FOO))
        self.assertTrue(self.__dispatcher.has_listeners(self.POST_FOO))
        self.__dispatcher.remove_subscriber(event_subscriber)
        self.assertFalse(self.__dispatcher.has_listeners(self.PRE_FOO))
        self.assertFalse(self.__dispatcher.has_listeners(self.POST_FOO))

    def _remove_subscriber_with_priorities(self):
        event_subscriber = TestEventSubscriberWithPriorities()
        self.__dispatcher.add_subscriber(event_subscriber)
        self.assertTrue(self.__dispatcher.has_listeners(self.PRE_FOO))
        self.__dispatcher.remove_subscriber(event_subscriber)
        self.assertFalse(self.__dispatcher.has_listeners(self.PRE_FOO))

    def _remove_subscriber_with_multiple_listeners(self):
        event_subscriber = TestEventSubscriberWithMultipleListeners()
        self.__dispatcher.add_subscriber(event_subscriber)
        self.assertTrue(self.__dispatcher.has_listeners(self.PRE_FOO))
        self.assertEqual(2, len(self.__dispatcher.get_listeners(self.PRE_FOO)))
        self.__dispatcher.remove_subscriber(event_subscriber)
        self.assertFalse(self.__dispatcher.has_listeners(self.PRE_FOO))

    def _event_receives_the_dispatcher_instance_as_argument(self):
        listener = TestWithDispatcher()
        self.__dispatcher.add_listener('test', getattr(listener, 'foo'))
        self.assertIsNone(listener.name)
        self.assertIsNone(listener.dispatcher)
        self.__dispatcher.dispatch('test')
        self.assertEqual('test', listener.name)
        self.assertEqual(self.__dispatcher, listener.dispatcher)

    def _has_listeners_when_added_callback_listener_is_removed(self):
        def listener():
            pass
        self.__dispatcher.add_listener('foo', listener)
        self.__dispatcher.remove_listener('foo', listener)
        self.assertFalse(self.__dispatcher.has_listeners())

    def _get_listeners_when_added_callback_listener_is_removed(self):
        def listener():
            pass
        self.__dispatcher.add_listener('foo', listener)
        self.__dispatcher.remove_listener('foo', listener)
        self.assertEqual({}, self.__dispatcher.get_listeners())

    def _has_listeners_without_events_returns_false_after_has_listeners_with_event_has_been_called(self):
        self.assertFalse(self.__dispatcher.has_listeners('foo'))
        self.assertFalse(self.__dispatcher.has_listeners())


class TestEventListener(object):

    def __init__(self):
        self.pre_foo_invoked = False
        self.post_foo_invoked = False

    def pre_foo(self, event: Event, event_name, dispatcher):
        self.pre_foo_invoked = True

    def post_foo(self, event: Event, event_name, dispatcher):
        self.post_foo_invoked = True
        event.stop_propagation()


class TestWithDispatcher(object):
    def __init__(self):
        self.name = None
        self.dispatcher = None

    def foo(self, event: Event, event_name, dispatcher):
        self.name = event_name
        self.dispatcher = dispatcher


class TestEventSubscriber(AbstractEventSubscriber):
    @staticmethod
    def get_subscribed_events():
        return {'pre.foo': 'pre_foo', 'post.foo': 'post_foo'}

    def pre_foo(self):
        pass

    def post_foo(self):
        pass


class TestEventSubscriberWithPriorities(AbstractEventSubscriber):
    @staticmethod
    def get_subscribed_events():
        return {
            'pre.foo':  ['pre_foo1', 10],
            'post.foo': ['pre_foo2']
        }

    def pre_foo1(self):
        pass

    def pre_foo2(self):
        pass


class TestEventSubscriberWithMultipleListeners(AbstractEventSubscriber):
    @staticmethod
    def get_subscribed_events():
        return {'pre.foo': [
            ['pre_foo1'],
            ['pre_foo2', 10]
        ]}

    def pre_foo1(self):
        pass

    def pre_foo2(self):
        pass


class TestEvent(Event):
    times_invoked = 0

    def invoke(self):
        self.times_invoked += 1
