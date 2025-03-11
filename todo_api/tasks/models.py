from django.contrib.auth.models import User
from django.db import models
from tasks.fields import HashAutoField


class Category(models.Model):
    id = HashAutoField()
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'
        verbose_name = 'Category'


class Task(models.Model):
    class Status(models.TextChoices):
        TODO = "TODO", "To Do"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        DONE = "DONE", "Done"

    id = HashAutoField()
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    categories = models.ManyToManyField(Category, related_name='tasks', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=11, choices=Status.choices, default=Status.TODO
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Tasks'
        verbose_name = 'Task'
        ordering = ['-due_date']
