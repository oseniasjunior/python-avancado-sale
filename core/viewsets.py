from rest_framework import viewsets
from rest_framework.decorators import action
from core import models, serializers, actions, behaviors
from decimal import Decimal


class StateViewSet(viewsets.ModelViewSet):
    queryset = models.State.objects.all()
    serializer_class = serializers.StateSerializer

    @action(methods=['GET'], detail=False)
    def get_by_name(self, request, *args, **kwargs):
        name = request.query_params.get('name')
        self.queryset = models.State.objects.filter(name__icontains=name)
        # result_serializer = serializers.StateSerializer(instance=queryset, many=True)
        # return Response(data=result_serializer.data, status=200)
        return super(StateViewSet, self).list(request, *args, **kwargs)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = models.Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer

    @action(methods=['GET'], detail=False)
    def get_by_department(self, request, *args, **kwargs):
        department = request.query_params.get('department')
        self.queryset = models.Employee.objects.filter(department__name__icontains=department)
        return super(EmployeeViewSet, self).list(request, *args, **kwargs)

    @action(methods=['PATCH'], detail=True)
    def upgrade_salary(self, request, *args, **kwargs):
        upgrade_percentage = request.data.pop('upgrade_percentage')
        # request.data['salary'] = actions.EmployeeActions.upgrade_salary(self.get_object(), upgrade_percentage)
        employee: 'models.Employee' = self.get_object()
        request.data['salary'] = employee.upgrade_salary(upgrade_percentage)
        # behavior_instance = behaviors.BaixaNoEstoqueBehavior(sale='')
        # behavior_instance.run()

        return super(EmployeeViewSet, self).partial_update(request, *args, **kwargs)


class BranchViewSet(viewsets.ModelViewSet):
    queryset = models.Branch.objects.all()
    serializer_class = serializers.BranchSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = models.Department.objects.all()
    serializer_class = serializers.DepartmentSerializer
