import logging
from django.utils.timezone import now
from rest_framework import serializers
from tasks.models import Category, Task


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели категорий."""

    class Meta:
        model = Category
        fields = ["id", "name"]


class TaskSerializer(serializers.ModelSerializer):
    """
    The serializer for a task model.

    - supports the automatic purpose of the user.
    - allows you to work with categories through the list of lines.
    - Includes checks of the uniqueness of the name and correctness of the date of execution.
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    categories = serializers.ListField(
        child=serializers.CharField(max_length=50), write_only=True, required=False
    )
    category_objects = CategorySerializer(
        source="categories", many=True, read_only=True
    )

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "user",
            "categories",
            "category_objects",
            "created_at",
            "due_date",
            "status",
        ]

    def validate_title(self, value):
        """Checks the uniqueness of the name of the problem for the user."""
        user = self.context["request"].user
        task_id = self.instance.id if self.instance else None

        if Task.objects.filter(user=user, title=value).exclude(id=task_id).exists():
            raise serializers.ValidationError(
                "Задача с таким названием уже существует."
            )
        return value

    def validate_due_date(self, value):
        """Checks that the date of execution is no earlier than the date of creation or the current date."""
        created_at = self.instance.created_at if self.instance else now()
        if value < created_at or value < now():
            raise serializers.ValidationError(
                "Дата выполнения не может быть в прошлом."
            )
        return value

    def validate_categories(self, value):
        """Checks the correctness of the transferred list of categories."""
        if not isinstance(value, list):
            raise serializers.ValidationError(
                "Поле 'categories' должно быть списком строк."
            )

        categories = [name.strip().title() for name in value if name.strip()]
        if not categories:
            raise serializers.ValidationError(
                "Список 'categories' не может быть пустым."
            )

        logging.info(value)
        return categories

    def get_or_create_categories(self, category_names):
        """
        Receives existing categories or creates new ones, if they are not.

        Returns a list of categories objects.
        """
        existing_categories = {
            cat.name: cat for cat in Category.objects.filter(name__in=category_names)
        }
        new_categories = [
            Category(name=name)
            for name in category_names
            if name not in existing_categories
        ]
        created_categories = Category.objects.bulk_create(
            new_categories, ignore_conflicts=True
        )
        return list(existing_categories.values()) + created_categories

    def create(self, validated_data):
        """Creates a new task with categories."""
        category_names = validated_data.pop("categories", [])
        categories = self.get_or_create_categories(category_names)
        logging.info(categories)

        task = Task.objects.create(**validated_data)
        task.categories.set(categories)
        return task

    def update(self, instance, validated_data):
        """Updates or creates the following categories, if they pass."""
        if "categories" in validated_data:
            category_names = validated_data.pop("categories", [])
            categories = self.get_or_create_categories(category_names)
            instance.categories.set(categories)

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        """Transforms the object of the problem for the output, replacing 'Category_objects' with 'Categories'."""
        data = super().to_representation(instance)
        data["categories"] = data.pop("category_objects")
        return data
