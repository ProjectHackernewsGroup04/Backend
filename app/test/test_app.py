import unittest
from app.controller import insert_post


class TestController(unittest.TestCase):
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_insert_post(self):
        obj = {'post_title': 'Y Combinator', 'post_text': '', 'hanesst_id': 1, 'post_type': 'story', 'post_parent': -1,
               'post_url': 'http://ycombinator.com', 'auth': "Basic b'cGc6WTg5S0lKM2ZyTQ=='"}
        returned = insert_post(obj)
        self.assertIsNotNone(returned)

        obj = {'post_title': '', 'post_text': 'hejwew', 'hanesst_id': 2, 'post_type': 'comment', 'post_parent': 1,
               'post_url': '', 'auth': "Basic b'cGc6WTg5S0lKM2ZyTQ=='"}

        returned = insert_post(obj)
        self.assertEqual(returned['id'], 2)

        obj = {'post_title': '', 'post_text': 'hejwew', 'hanesst_id': 3, 'post_type': 'comment', 'post_parent': 2,
               'post_url': '', 'auth': "Basic b'cGc6WTg5S0lKM2ZyTQ=='"}

        self.assertEqual(obj)


if __name__ == '__main__':
    unittest.main()
