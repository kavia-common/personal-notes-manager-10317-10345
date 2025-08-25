from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User


class HealthTests(APITestCase):
    def test_health(self):
        url = reverse('Health')  # Make sure the URL is named
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"message": "Server is up!"})


class NotesAuthCrudTests(APITestCase):
    def setUp(self):
        self.username = "alice"
        self.password = "secret123"
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_register_and_login_and_crud(self):
        # Register a new user
        reg_url = reverse("Register")
        resp = self.client.post(reg_url, {"username": "bob", "password": "password1"})
        self.assertIn(resp.status_code, (200, 201,))  # 201 expected

        # Login with existing user
        login_url = reverse("Login")
        resp = self.client.post(login_url, {"username": self.username, "password": self.password})
        self.assertEqual(resp.status_code, 200)

        # Create a note
        create_url = "/api/notes/"
        resp = self.client.post(create_url, {"title": "My Note", "content": "Content"})
        self.assertEqual(resp.status_code, 201, resp.content)
        note_id = resp.data["id"]

        # List notes
        resp = self.client.get(create_url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 1)

        # Retrieve note
        resp = self.client.get(f"/api/notes/{note_id}/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["title"], "My Note")

        # Update note
        resp = self.client.patch(f"/api/notes/{note_id}/", {"title": "Updated"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["title"], "Updated")

        # Delete note
        resp = self.client.delete(f"/api/notes/{note_id}/")
        self.assertIn(resp.status_code, (200, 204))
