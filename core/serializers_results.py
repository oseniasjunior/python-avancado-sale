from rest_framework import serializers


class TotalEmployeeSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    count = serializers.IntegerField(read_only=True)
