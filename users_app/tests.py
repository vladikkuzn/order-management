from django.test import Client, TestCase


class UserBaseAuthTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.account_data = {
            'password': '123',
            'username': 'admin',
            'first_name': 'admin',
            'last_name': 'adminovich',
            'email': 'admin@e.com',
            'role': '',
        }

    def test_register(self):
        response = self.client.post('/register/', self.account_data)
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        response = self.client.post('/login/', self.account_data)
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.client.post('/logout/')
        self.assertEqual(response.status_code, 302)
