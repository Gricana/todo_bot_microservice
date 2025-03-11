from django.contrib import admin
from django.contrib.auth.models import User
from tasks.admin import TaskInline
from tasks.models import Task


admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    """
    Admin panel for users.

    - displays the number of urgent (not completed) tasks.
    - Allows you to look for users by name and email.
    - Includes a built -in list of user tasks.
    """

    list_display = ("username", "email", "task_count")
    search_fields = ("username", "email")
    inlines = [TaskInline]
    list_per_page = 50

    def task_count(self, obj):
        """
        Counts the number of active user tasks.
        """
        return obj.tasks.exclude(status=Task.Status.DONE).count()

    task_count.short_description = "Всего актуальных задач"
