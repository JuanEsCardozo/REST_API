import unittest
import json
from app import app

class TestAPI(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_department_endpoint(self):
        response = self.app.post('/upload/departments')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Data Successfully Uploaded')

if _name_ == '_main_':
   unittest.main()