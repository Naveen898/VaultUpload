import unittest
from backend.services.jwt_service import generate_token, validate_token
from backend.services.auth_service import UserService

class TestAuth(unittest.TestCase):

    def setUp(self):
        self.user_service = UserService()
        self.test_user = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        self.token = generate_token(self.test_user['username'])

    def test_generate_token(self):
        token = generate_token(self.test_user['username'])
        self.assertIsNotNone(token)

    def test_validate_token_success(self):
        is_valid = validate_token(self.token)
        self.assertTrue(is_valid)

    def test_validate_token_failure(self):
        invalid_token = 'invalid.token.string'
        is_valid = validate_token(invalid_token)
        self.assertFalse(is_valid)

    def test_user_login_success(self):
        self.user_service.create_user(self.test_user['username'], self.test_user['password'])
        token = self.user_service.login(self.test_user['username'], self.test_user['password'])
        self.assertIsNotNone(token)

    def test_user_login_failure(self):
        token = self.user_service.login(self.test_user['username'], 'wrongpassword')
        self.assertIsNone(token)

if __name__ == '__main__':
    unittest.main()