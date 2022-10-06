from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer
from core import models


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.State
        fields = '__all__'


class MaritalStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MaritalStatus
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Department
        fields = '__all__'

    def validate(self, attrs):
        pass
        # actions.SaleItemActions.regra()

        # behavior = behaviors.SaleItemBehavior()
        # behavior.run()


class EmployeeSerializer(FlexFieldsModelSerializer):
    # marital_status_obj = MaritalStatusSerializer(
    #     source='marital_status',
    #     read_only=True
    # )
    # marital_status_name = serializers.SlugRelatedField(
    #     read_only=True,
    #     source='marital_status',
    #     slug_field='name'
    # )
    # department_obj = DepartmentSerializer(
    #     source='department',
    #     read_only=True
    # )

    class Meta:
        model = models.Employee
        fields = '__all__'
        expandable_fields = {
            'marital_status': ('core.MaritalStatusSerializer',),
            'department': ('core.DepartmentSerializer',)
        }


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Branch
        fields = '__all__'


# class ZoneSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     active = serializers.BooleanField(default=True)
#     modified_at = serializers.DateTimeField(required=False)
#     created_at = serializers.DateTimeField(required=False)
#     name = serializers.CharField(required=True, max_length=64)
#
#     # departments = serializers.ListField(
#     #     required=False,
#     #     child=serializers.CharField()
#     # )
#
#     def validate(self, attrs: dict):
#         if not attrs.get('name').isupper():
#             raise Exception('O campo deve ser em maiúsculo')
#         return super(ZoneSerializer, self).validate(attrs)
#
#     def create(self, validated_data: dict):
#         # departments = validated_data.pop('departments')
#         zone = models.Zone()
#         for key, value in validated_data.items():
#             setattr(zone, key, value)
#         zone.save()
#         return zone
#
#     def update(self, instance, validated_data):
#         for key, value in validated_data.items():
#             setattr(instance, key, value)
#         instance.save()
#         return instance


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Sale
        fields = '__all__'


class SaleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SaleItem
        fields = '__all__'


class CitySerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.City
        fields = '__all__'

    expandable_fields = {
        'state': ('core.StateSerializer',)
    }


class DistrictSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.District
        fields = '__all__'

    expandable_fields = {
        'city': ('core.CitySerializer',),
        'zone': ('core.ZoneSerializer',)
    }
