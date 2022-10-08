from rest_framework import serializers


class UpgradeSalarySerializer(serializers.Serializer):
    upgrade_percentage = serializers.DecimalField(
        required=True,
        allow_null=False,
        max_digits=10,
        decimal_places=2
    )


class LongTimeTaskSerializer(serializers.Serializer):
    long_time_task = serializers.IntegerField(required=True)
