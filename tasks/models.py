from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
    ]

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("IN_PROGRESS", "In Progress"),
        ("COMPLETED", "Completed"),
    ]

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="MEDIUM")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to="tasks/", null=True, blank=True)

    # Used for kanban drag & drop ordering
    order = models.PositiveIntegerField(default=0, db_index=True)

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_tasks",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "created_at"]

    def __str__(self):
        return f"[{self.code}] {self.name}"
