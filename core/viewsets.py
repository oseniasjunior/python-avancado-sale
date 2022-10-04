from rest_framework import viewsets
from core import models, serializers


class StateViewSet(viewsets.ModelViewSet):
    queryset = models.State.objects.all()
    serializer_class = serializers.StateSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = models.Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer


class BranchViewSet(viewsets.ModelViewSet):
    queryset = models.Branch.objects.all()
    serializer_class = serializers.BranchSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = models.Department.objects.all()
    serializer_class = serializers.DepartmentSerializer
