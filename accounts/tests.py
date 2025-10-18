# accounts/tests/test_accounts_views.py
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import tag
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

User = get_user_model()


class AccountsViewsTests(APITestCase):
    """
    Basic happy-path and error-path tests for the auth endpoints:
    /register, /login, /refresh, /me, /logout (SimpleJWT).
    """

    def setUp(self):
        self.client = APIClient()

        # Named routes from your urls.py
        self.url_register = reverse("user_register")
        self.url_login = reverse("user_login")
        self.url_refresh = reverse("token_refresh")
        self.url_me = reverse("user_me")
        self.url_logout = reverse("user_logout")

        self.password = "TestPass123!"
        self.user = User.objects.create_user(
            username="hollie",
            email="hollie@example.com",
            first_name="Hollie",
            last_name="Morrison",
            password=self.password,
        )

    # ---------- Helpers ----------
    def _login_and_get_tokens(self, username=None, password=None):
        """Helper: Log in and return (access, refresh) tokens."""
        res = self.client.post(
            self.url_login,
            {
                "username": username or self.user.username,
                "password": password or self.password,
            },
            format="json",
        )
        self.assertEqual(
            res.status_code,
            status.HTTP_200_OK,
            msg=f"Login failed. Response: {res.data}",
        )
        return res.data["access"], res.data["refresh"]

    # ---------- Register ----------
    @tag("register", "smoke")
    def test_register_success(self):
        """Register: returns 201 + tokens + user payload when inputs are valid."""
        payload = {
            "username": "newuser",
            "email": "newuser@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "NewUserPass123!",
            "password2": "NewUserPass123!",
        }
        res = self.client.post(self.url_register, payload, format="json")

        self.assertEqual(
            res.status_code, status.HTTP_201_CREATED, msg=f"Errors: {res.data}"
        )
        self.assertIn("access", res.data, "Missing access token in response")
        self.assertIn("refresh", res.data, "Missing refresh token in response")
        self.assertIn("user", res.data, "Missing user object in response")
        self.assertEqual(res.data["user"]["username"], "newuser")
        self.assertTrue(User.objects.filter(username="newuser").exists())
        self.assertNotIn("password", res.data["user"], "Password leaked in response")

    @tag("register")
    def test_register_validation_error_missing_password2(self):
        """Register: returns 400 if password2 is missing (serializer requirement)."""
        payload = {
            "username": "nouserpwd",
            "email": "no@pwd.com",
            "first_name": "No",
            "last_name": "Pwd",
            "password": "NewUserPass123!",
        }
        res = self.client.post(self.url_register, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST, msg=res.data)
        self.assertIn("password2", res.data, "Expected 'password2' error")

    @tag("register")
    def test_register_password_mismatch(self):
        """Register: returns 400 if password and password2 do not match."""
        payload = {
            "username": "mismatch",
            "email": "mismatch@example.com",
            "first_name": "Mis",
            "last_name": "Match",
            "password": "NewUserPass123!",
            "password2": "DifferentPass123!",
        }
        res = self.client.post(self.url_register, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST, msg=res.data)
        self.assertIn("password2", res.data, "Expected 'password2' mismatch error")

    # ---------- Login ----------
    @tag("login", "smoke")
    def test_login_success(self):
        """Login: returns 200 + tokens + user payload with correct credentials."""
        res = self.client.post(
            self.url_login,
            {"username": self.user.username, "password": self.password},
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK, msg=res.data)
        self.assertIn("access", res.data)
        self.assertIn("refresh", res.data)
        self.assertIn("user", res.data)
        self.assertEqual(res.data["user"]["username"], self.user.username)

    @tag("login")
    def test_login_missing_fields(self):
        """Login: returns 400 if username or password is missing."""
        res = self.client.post(self.url_login, {"username": self.user.username}, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST, msg=res.data)
        self.assertIn("detail", res.data)

    @tag("login")
    def test_login_invalid_credentials(self):
        """Login: returns 401 if credentials are invalid."""
        res = self.client.post(
            self.url_login, {"username": self.user.username, "password": "wrong"}, format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED, msg=res.data)
        self.assertIn("detail", res.data)

    # ---------- Me ----------
    @tag("me")
    def test_me_requires_auth(self):
        """Me: returns 401 without Authorization header."""
        res = self.client.get(self.url_me)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    @tag("me", "smoke")
    def test_me_with_valid_access_token(self):
        """Me: returns 200 + user data when given a valid Bearer token."""
        access, _ = self._login_and_get_tokens()
        res = self.client.get(self.url_me, HTTP_AUTHORIZATION=f"Bearer {access}")
        self.assertEqual(res.status_code, status.HTTP_200_OK, msg=res.data)
        self.assertEqual(res.data.get("username"), self.user.username)

    # ---------- Logout ----------
    @tag("logout")
    def test_logout_requires_auth(self):
        """Logout: returns 401 if no Authorization header is provided."""
        res = self.client.post(self.url_logout, {"refresh": "dummy"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    @tag("logout", "smoke")
    def test_logout_with_refresh_token(self):
        """Logout: returns 205 when provided a valid refresh token + auth header."""
        access, refresh = self._login_and_get_tokens()
        res = self.client.post(
            self.url_logout,
            {"refresh": refresh},
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {access}",
        )
        self.assertEqual(res.status_code, status.HTTP_205_RESET_CONTENT, msg=res.data)

    @tag("logout")
    def test_logout_missing_refresh_token(self):
        """Logout: returns 400 if refresh token is missing from body."""
        access, _ = self._login_and_get_tokens()
        res = self.client.post(self.url_logout, {}, format="json", HTTP_AUTHORIZATION=f"Bearer {access}")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST, msg=res.data)
        self.assertIn("detail", res.data)

    # ---------- Token Refresh ----------
    @tag("refresh", "smoke")
    def test_token_refresh_success(self):
        """Refresh: returns 200 and a new access token when given a valid refresh."""
        _, refresh = self._login_and_get_tokens()
        res = self.client.post(self.url_refresh, {"refresh": refresh}, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK, msg=res.data)
        self.assertIn("access", res.data)

    @tag("refresh")
    def test_token_refresh_requires_body(self):
        """Refresh: returns 400 if no refresh token is provided in the body."""
        res = self.client.post(self.url_refresh, {}, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST, msg=res.data)
