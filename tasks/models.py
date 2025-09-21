from django.db import models

# Create your models here.
# app_name/models.py
from __future__ import annotations

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class TaskQuerySet(models.QuerySet):
    # States
    def open(self):
        return self.filter(state=Task.State.OPEN)

    def in_progress(self):
        return self.filter(state=Task.State.IN_PROGRESS)

    def done(self):
        return self.filter(state=Task.State.DONE)

    # Time-based
    def overdue(self):
        now = timezone.now()
        return self.exclude(state=Task.State.DONE).filter(
            models.Q(is_overdue=True) | models.Q(due_date__lt=now)
        )

    def due_by(self, dt):
        return self.filter(due_date__lte=dt)

    # Faceted filters
    def with_priority(self, priority: int):
        return self.filter(priority=priority)

    def with_category(self, category: "Category | int | str"):
        if isinstance(category, Category):
            return self.filter(category=category)
        if isinstance(category, int):
            return self.filter(category_id=category)
        return self.filter(category__name__iexact=category)

    def owned_by(self, user):
        return self.filter(owners=user)

    def created_by(self, user):
        return self.filter(created_by=user)


class Task(models.Model):
    class Priority(models.IntegerChoices):
        LOW = 1, "Low"
        MEDIUM = 2, "Medium"
        HIGH = 3, "High"
        URGENT = 4, "Urgent"

    class State(models.TextChoices):
        OPEN = "open", "Open"
        IN_PROGRESS = "in_progress", "In progress"
        DONE = "done", "Done"
        CANCELLED = "cancelled", "Cancelled"

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    # Ownership
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="created_tasks",
        on_delete=models.CASCADE,
    )
    owners = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="owned_tasks",
        blank=True,
        help_text="Users responsible for this task.",
    )

    # Classification
    priority = models.PositiveSmallIntegerField(
        choices=Priority.choices, default=Priority.MEDIUM, db_index=True
    )
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL, related_name="tasks"
    )
    state = models.CharField(
        max_length=20, choices=State.choices, default=State.OPEN, db_index=True
    )

    # Scheduling
    due_date = models.DateTimeField(null=True, blank=True, db_index=True)
    is_overdue = models.BooleanField(
        default=False,
        help_text="Manual override; also auto-syncs from due_date/state on save().",
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Manager
    objects = TaskQuerySet.as_manager()

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["state", "priority"]),
            models.Index(fields=["due_date"]),
        ]

    def __str__(self) -> str:
        return f"{self.title} (#{self.pk})"

    @property
    def computed_overdue(self) -> bool:
        if self.state == self.State.DONE or not self.due_date:
            return False
        return self.due_date < timezone.now()

    def clean(self):
        if self.due_date and self.created_at and self.due_date < self.created_at:
            raise ValidationError({"due_date": "Due date cannot be before creation time."})

    def save(self, *args, **kwargs):
        if self.state == self.State.DONE:
            self.is_overdue = False
        elif self.due_date:
            self.is_overdue = self.due_date < timezone.now()
        super().save(*args, **kwargs)
