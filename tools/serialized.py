# tools/serializers.py
from rest_framework import serializers

class FileSerializer(serializers.Serializer):
    filename = serializers.CharField(max_length=255)
    content = serializers.CharField(required=False, allow_blank=True)

class WriteFileSerializer(serializers.Serializer):
    filename = serializers.CharField(max_length=255)
    content = serializers.CharField()