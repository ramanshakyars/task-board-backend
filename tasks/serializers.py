from accounts.serializers import UserSerializer
from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            "id",
            "name",
            "code",
            "priority",
            "status",
            "description",
            "due_date",
            "image",
            "image_url",
            "order",
            "created_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_by", "created_at", "updated_at", "order"]

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None


class TaskCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = [
            "name",
            "code",
            "priority",
            "status",
            "description",
            "due_date",
            "image",
        ]


class TaskStatusUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ["status"]


class TaskReorderSerializer(serializers.Serializer):

    ordered_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
    )
