from rest_framework import serializers

class CodeExecutionSerializer(serializers.Serializer):
    code = serializers.CharField()