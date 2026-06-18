from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import OPEN, Project


class ProjectSerializer(serializers.ModelSerializer):
    client = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Project
        fields = ["id", "client", "title", "description", "budget", "deadline", "status", "created_at"]
        read_only_fields = ["id", "client", "status", "created_at"]

    def validate_title(self, value):
        value = value.strip()
        if not value:
            raise ValidationError("Project title kiritilishi shart.")
        return value

    def create(self, validated_data):
        validated_data["status"] = OPEN
        return super().create(validated_data)
