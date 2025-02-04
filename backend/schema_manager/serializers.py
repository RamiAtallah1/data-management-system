from rest_framework import serializers
from .models import Schema


class SchemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schema
        fields = "__all__"
