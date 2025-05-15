from django.test import TestCase
from django.urls import reverse, resolve

class ApiUrlTests(TestCase):
    def check_and_print(self, name, condition):
        if condition:
            print(f"TEST {name}: TRUE")
        else:
            print(f"TEST {name}: FALSE")
        self.assertTrue(condition)

    def test_api_register_url(self):
        try:
            url = reverse('db_app:api_register')
            match = resolve(url)
            self.check_and_print('api_register_url', match is not None)
        except Exception as e:
            print(f"TEST api_register_url: FALSE (Exception: {e})")
            self.assertTrue(False)

    def test_api_token_url(self):
        try:
            url = reverse('db_app:token_obtain_pair')
            match = resolve(url)
            self.check_and_print('api_token_url', match is not None)
        except Exception as e:
            print(f"TEST api_token_url: FALSE (Exception: {e})")
            self.assertTrue(False)

    def test_api_token_refresh_url(self):
        try:
            url = reverse('db_app:token_refresh')
            match = resolve(url)
            self.check_and_print('api_token_refresh_url', match is not None)
        except Exception as e:
            print(f"TEST api_token_refresh_url: FALSE (Exception: {e})")
            self.assertTrue(False)

    def test_api_user_url(self):
        try:
            url = reverse('db_app:api_user')
            match = resolve(url)
            self.check_and_print('api_user_url', match is not None)
        except Exception as e:
            print(f"TEST api_user_url: FALSE (Exception: {e})")
            self.assertTrue(False)
