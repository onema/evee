from unittest import TestCase
from evee.generic_event import GenericEvent


class GenericEventTest(TestCase):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.__event = None
        self.__subject = None

    def setUp(self):
        self.__subject = object()  # type: object
        self.__event = GenericEvent(self.__subject, {'name': 'Event'})  # type: GenericEvent

    def tearDown(self):
        self.__subject = None
        self.__event = None

    def test_construct(self):
        self.assertEqual(self.__event, GenericEvent(self.__subject, {'name': 'Event'}))

    def test_get_arguments(self):
        self.assertEqual({'name': 'Event'}, self.__event.get_arguments())

    def test_set_arguments(self):
        result = self.__event.set_arguments({'foo': 'bar'})
        self.assertEqual(dict(foo='bar'), self.__event.get_arguments())
        self.assertEqual(self.__event, result)

    def test_set_argument(self):
        self.__event.set_argument('foo2', 'bar2')
        self.assertEqual({'name': 'Event', 'foo2': 'bar2'}, self.__event.get_arguments())

    def test_get_argument(self):
        self.assertEqual('Event', self.__event.get_argument('name'))

    def test_get_arg_exception(self):
        with self.assertRaises(KeyError):
            self.__event.get_argument('name does not exist')

    def test_offset_get(self):
        self.assertEqual('Event', self.__event['name'])

        with self.assertRaises(KeyError):
            self.assertFalse(self.__event['name does not exist'])

    def test_offset_set(self):
        self.__event['foo2'] = 'bar2'
        self.assertEqual({'name': 'Event', 'foo2': 'bar2'}, self.__event.get_arguments())

    def test_offset_del(self):
        del(self.__event['name'])
        self.assertEqual({}, self.__event.get_arguments())

    def test_key_in_event(self):
        self.assertTrue(('name' in self.__event))
        self.assertFalse(('name does not exist' in self.__event))

    def test_has_argument(self):
        self.assertTrue(self.__event.has_argument('name'))
        self.assertFalse(self.__event.has_argument('name does not exist'))

    def test_get_subject(self):
        self.assertEqual(self.__subject, self.__event.get_subject())

    def test_has_iterator(self):
        data = {}
        for key, value in self.__event.items():
            data[key] = value

        self.assertEqual({'name': 'Event'}, data)
