import json
import uuid
from faker import Faker
from unittest import TestCase
from app import create_app
from db import db
from unittest.mock import patch

class TestAddEmailBacklist(TestCase):

    def setUp(self):
        super().setUp()
        app = create_app(database='sqlite:///:memory:')
        self.client = app.test_client()
        self.faker = Faker()
        self.app_ctx = app.app_context()
        self.app_ctx.push()
        db.create_all()

        # Bearer token
        self.bearer_token_valid = 'Bearer VerifyToken1234'
        self.bearer_token_invalid = self.faker.sha256()

        self.data = {
            "email": self.faker.email(),
            "app_uuid": str(uuid.uuid4()),
            "blocked_reason": self.faker.word()
        }
        
    def tearDown(self):
        self.app_ctx.pop()
        del self.app_ctx

    @patch('requests.get')  
    def test_add_email_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"id": str(uuid.uuid4())}

        response = self.client.post('/blacklists', data=json.dumps(self.data),
                                headers={'Authorization': self.bearer_token_valid})

        # Verificación de la respuesta
        self.assertEqual(response.status_code, 201)
        
    @patch('requests.get')  
    def test_add_email_invalid_token(self, mock_get):
        mock_get.return_value.status_code = 401
        mock_get.return_value.json.return_value = {"id": str(uuid.uuid4())}

        response = self.client.post('/blacklists', data=json.dumps(self.data),
                                headers={'Authorization': self.bearer_token_invalid})

        # Verificación de la respuesta
        self.assertEqual(response.status_code, 401)
        
    @patch('requests.get')  
    def test_add_email_invalid_data(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"id": str(uuid.uuid4())}

        self.data["email"] = None
        response = self.client.post('/blacklists', data=json.dumps(self.data),
                                headers={'Authorization': self.bearer_token_valid})

        # Verificación de la respuesta
        self.assertEqual(response.status_code, 400)