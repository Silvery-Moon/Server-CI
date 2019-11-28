import unittest
import json
from socket_server import app


class BasicTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False

        self.app = app.test_client()
        self.assertEqual(app.debug, False)

    def tearDown(self):
        pass

    def test_test(self):
        response = self.app.put('/', data='{"key": "1", "message": "23"}', follow_redirects=True)
        self.assertEqual(response.status_code, 404)

        response = self.app.get('/', data='{"key": "1"}', follow_redirects=True)
        self.assertEqual(response.status_code, 404)

        response = self.app.post('/', data='{"key": "1", "message": "23"}', follow_redirects=True)
        self.assertEqual(response.status_code, 201)

        response = self.app.get('/', data='{"key": "1"}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual("23", json.loads(str(response.get_data().decode("utf-8").strip())).get("message"))

        response = self.app.post('/', data='{"key": "1", "message": "34"}', follow_redirects=True)
        self.assertEqual(response.status_code, 405)

        response = self.app.get('/', data='{"key": "1"}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual("23", json.loads(str(response.get_data().decode("utf-8").strip())).get("message"))

        response = self.app.put('/', data='{"key": "1", "message": "34"}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/', data='{"key": "1"}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual("34", json.loads(str(response.get_data().decode("utf-8").strip())).get("message"))

        response = self.app.delete('/', data='{"key": "1"}', follow_redirects=True)
        self.assertEqual(response.status_code, 204)

        response = self.app.get('/', data='{"key": "1"}', follow_redirects=True)
        self.assertEqual(response.status_code, 404)

        response = self.app.delete('/', data='{"key": "1"}', follow_redirects=True)
        self.assertEqual(response.status_code, 204)

        response = self.app.get('/', data='{"key": "1"}', follow_redirects=True)
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
