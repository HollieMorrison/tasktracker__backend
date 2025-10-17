from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from tasks.models import Task, Category 


class TaskApiTests(APITestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username="testuser", password="pass1234", email="user@example.com"
        )
        self.category = Category.objects.create(name="Work")
        self.client.force_authenticate(self.user)
        self.list_url = reverse("task_list")

    # -------------------------
    # Authentication
    # -------------------------
    def test_auth_required(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # -------------------------
    # Create
    # -------------------------
    def test_create_task(self):
        payload = {
            "title": "New Task",
            "description": "Test description",
            "priority": Task.Priority.MEDIUM,
            "state": Task.State.OPEN,
            "category": self.category.id,
            "due_date": (timezone.now() + timezone.timedelta(days=1)).isoformat(),
        }
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        task = Task.objects.get(id=response.data["id"])
        self.assertEqual(task.title, "New Task")
        self.assertEqual(task.created_by, self.user)

    # -------------------------
    # List
    # -------------------------
    def test_list_tasks(self):
        Task.objects.create(title="Task 1", created_by=self.user)
        Task.objects.create(title="Task 2", created_by=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    # -------------------------
    # Retrieve single
    # -------------------------
    def test_retrieve_task(self):
        task = Task.objects.create(title="My Task", created_by=self.user)
        url = reverse("task_detail", args=[task.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "My Task")

    # -------------------------
    # Update (PATCH)
    # -------------------------
    def test_update_task(self):
        task = Task.objects.create(title="Old Title", created_by=self.user)
        url = reverse("task_detail", args=[task.id])
        response = self.client.patch(url, {"title": "Updated Title"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        task.refresh_from_db()
        self.assertEqual(task.title, "Updated Title")

    # -------------------------
    # Full update (PUT)
    # -------------------------
    def test_full_update_task(self):
        task = Task.objects.create(title="Old", created_by=self.user, category=self.category)
        url = reverse("task_detail", args=[task.id])
        payload = {
            "title": "Completely Updated",
            "description": "Full update description",
            "priority": Task.Priority.HIGH,
            "state": Task.State.IN_PROGRESS,
            "category": self.category.id,
        }
        response = self.client.put(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        task.refresh_from_db()
        self.assertEqual(task.title, "Completely Updated")
        self.assertEqual(task.state, Task.State.IN_PROGRESS)

    # -------------------------
    # Delete
    # -------------------------
    def test_delete_task(self):
        task = Task.objects.create(title="Delete Me", created_by=self.user)
        url = reverse("task_detail", args=[task.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=task.id).exists())

    # -------------------------
    # Validation
    # -------------------------
    def test_due_date_cannot_be_before_creation(self):
        past_date = timezone.now() - timezone.timedelta(days=2)
        payload = {
            "title": "Invalid Task",
            "due_date": past_date.isoformat(),
            "category": self.category.id,
        }
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
