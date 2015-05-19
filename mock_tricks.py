import unittest

import mock


class Cheese(object):
    @property
    def name(self):
        return 'Cheddar'


class MyTestCase(unittest.TestCase):

    def test_subsequent_returns(self):
        # Set multiple side effects on a mock function to
        # simulate a sequence of return values
        mock_cheese = mock.Mock(side_effect=['cheddar', 'brie'])

        self.assertEqual(mock_cheese(), 'cheddar')
        self.assertEqual(mock_cheese(), 'brie')

    def test_mock_name_property(self):
        # If the thing you are mocking has a property named 'name',
        # make sure Mock doesn't steal it for its own purposes.

        # Nope! This won't work.
        # cheese = mock.Mock(name='yarg')

        # We have to do this instead.
        cheese = mock.Mock()
        cheese.configure_mock(name='yarg')

        self.assertEqual(cheese.name, 'yarg')

    def test_mock_read_only_property(self):
        cheese = Cheese()

        # Nope. Can't set attribute
        # cheese.name = mock.Mock(return_value='Brie')

        # type() and PropertyMock can get around this
        # This works, BUT this is bad as it will persist into later tests
        # type(cheese).name = mock.PropertyMock(return_value='Brie')
        # self.assertEqual(cheese.name, 'Brie')

        # Keep it scoped to the local test
        with mock.patch.object(Cheese, 'name',
                               new_callable=mock.PropertyMock) as mock_name:
            mock_name.return_value = 'Brie'
            self.assertEqual(cheese.name, 'Brie')

            # side_effect can still simulate multiple property values
            mock_name.side_effect = ['Yarg', 'Stilton']
            self.assertEqual(cheese.name, 'Yarg')
            self.assertEqual(cheese.name, 'Stilton')


if __name__ == '__main__':
    unittest.main()
