from django.contrib import admin
from django.contrib.auth import get_user_model
from tasks.models import Category, Task

User = get_user_model()


class TaskInline(admin.TabularInline):
    """
    Integrates the tasks in the administrative panel for users.

    Displays only the necessary fields, such as:
        - Title
        - Status
        - Due_Date
    """

    model = Task
    extra = 0
    fields = (
        'title',
        'status',
        'due_date',
    )
    ordering = (
        '-status',
        '-created_at',
    )
    readonly_fields = ('id',)
    show_change_link = True
    can_delete = True


def mark_done(modeladmin, request, queryset):
    """
    Check the selected tasks as completed.
    """
    queryset.update(status=Task.Status.DONE)


mark_done.short_description = "Пометить как выполненные"


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Class for setting up tasks in the administrative panel.

    Includes:
        - actions for the mark of the task as completed.
        - The ability to edit Title and Status.
    """

    list_display = (
        'short_id',
        'title',
        'description',
        'user',
        'status',
        'created_at',
        'due_date',
    )
    list_filter = ('status', 'user')
    search_fields = ('title', 'description')
    list_editable = (
        'title',
        'status',
    )
    ordering = (
        '-status',
        '-created_at',
    )
    autocomplete_fields = ('categories',)
    readonly_fields = (
        'id',
        'created_at',
    )
    actions = [mark_done]  # Action for marking tasks as completed
    list_per_page = 20

    def short_id(self, obj):
        """
        Returns the first 10 characters of ID tasks.

        Parameters:
            OBJ (TASK): a copy of the task.
        """
        return str(obj.id)[:10]

    short_id.short_description = "ID"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Class for setting up categories in the administrative panel.
    """

    list_display = ('name',)
    search_fields = ('name',)
    readonly_fields = ('id',)
    ordering = ('name',)
    list_per_page = 30


admin.site.site_header = "Сервис по мониторингу рабочих задач"
