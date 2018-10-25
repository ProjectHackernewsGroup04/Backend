import unittest
from controller import insert_post


class TestController(unittest.TestCase):
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_insert_post(self):
        obj = {'post_title': 'Y Combinator', 'post_text': '', 'hanesst_id': 1, 'post_type': 'story', 'post_parent': -1,
               'post_url': 'http://ycombinator.com', 'auth': "Basic b'cGc6WTg5S0lKM2ZyTQ=='"}
        returned = insert_post(obj)
        self.assertIsNotNone(returned)


if __name__ == '__main__':
    unittest.main()
