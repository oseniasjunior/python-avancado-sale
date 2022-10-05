from rest_framework import serializers
from core import models


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.State
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Employee
        fields = '__all__'


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Branch
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Department
        fields = '__all__'


class ZoneSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    active = serializers.BooleanField(default=True)
    modified_at = serializers.DateTimeField(required=False)
    created_at = serializers.DateTimeField(required=False)
    name = serializers.CharField(required=True, max_length=64)

    # departments = serializers.ListField(
    #     required=False,
    #     child=serializers.CharField()
    # )

    def validate(self, attrs: dict):
        if not attrs.get('name').isupper():
            raise Exception('O campo deve ser em maiúsculo')
        return super(ZoneSerializer, self).validate(attrs)

    def create(self, validated_data: dict):
        # departments = validated_data.pop('departments')
        zone = models.Zone()
        for key, value in validated_data.items():
            setattr(zone, key, value)
        zone.save()
        return zone

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance