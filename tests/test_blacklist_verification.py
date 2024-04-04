import json
import uuid
from faker import Faker
from unittest import TestCase
from app import create_app
from db import db
from models import BlacklistEmail
from unittest.mock import patch, MagicMock


class TestBlacklistEmailVerification(TestCase):

    def setUp(self):
        super().setUp()
        app = create_app(database='sqlite:///:memory:')
        self.client = app.test_client()
        self.faker = Faker()
        self.app_ctx = app.app_context()
        self.app_ctx.push()
        db.create_all()

        # Parametros de prueba
        self.not_blocked_email = self.faker.email()
        self.invalid_email = 'not_an_email'
        self.email = self.faker.email()
        self.app_uuid = str(uuid.uuid4())
        self.blocked_reason = self.faker.word()

        # Bearer token
        self.bearer_token_valid = 'Bearer VerifyToken1234'
        self.bearer_token_invalid = self.faker.sha256()

        # Crear email en lista negra
        self.create_blacklist_email()

    def create_blacklist_email(self):
        email = BlacklistEmail(
            email=self.email,
            app_uuid=self.app_uuid,
            blocked_reason=self.blocked_reason,
            ip_address=self.faker.ipv4(),
            created_at=self.faker.date_time()
        )
        db.session.add(email)
        db.session.commit()

    def tearDown(self):
        self.app_ctx.pop()
        del self.app_ctx

    def test_blacklist_email_no_token(self):
        response = self.client.get(f'/blacklists/{self.email}')
        self.assertEqual(response.status_code, 403)

    def test_blacklist_email_invalid_token(self):
        response = self.client.get(f'/blacklists/{self.email}',
                                   headers={'Authorization': self.bearer_token_invalid})
        self.assertEqual(response.status_code, 401)

    def test_blacklist_invalid_email(self):
        response = self.client.get(f'/blacklists/{self.invalid_email}',
                                   headers={'Authorization': self.bearer_token_valid})
        self.assertEqual(response.status_code, 400)

    def test_blacklist_email_blocked(self):
        response = self.client.get(f'/blacklists/{self.email}',
                                   headers={'Authorization': self.bearer_token_valid})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['is_blacklisted'])
        self.assertEqual(data['reason'], self.blocked_reason)

    def test_blacklist_email_not_blocked(self):
        response = self.client.get(f'/blacklists/{self.not_blocked_email}',
                                   headers={'Authorization': self.bearer_token_valid})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(data['is_blacklisted'])
        self.assertEqual(data['reason'], "The email is not in the blacklist")