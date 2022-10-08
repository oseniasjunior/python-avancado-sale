from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from core import models, serializers, actions, behaviors, serializers_params, serializers_results, filters, tasks
from decimal import Decimal


class StateViewSet(viewsets.ModelViewSet):
    queryset = models.State.objects.all()
    serializer_class = serializers.StateSerializer
    filterset_class = filters.StateFilter

    # @action(methods=['GET'], detail=False)
    # def get_by_name(self, request, *args, **kwargs):
    #     name = request.query_params.get('name')
    #     self.queryset = models.State.objects.filter(name__icontains=name)
    #     # result_serializer = serializers.StateSerializer(instance=queryset, many=True)
    #     # return Response(data=result_serializer.data, status=200)
    #     return super(StateViewSet, self).list(request, *args, **kwargs)


class MaritalStatusViewSet(viewsets.ModelViewSet):
    queryset = models.MaritalStatus.objects.all()
    serializer_class = serializers.MaritalStatusSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = models.Employee.objects.select_related('marital_status', 'department').all()
    serializer_class = serializers.EmployeeSerializer
    filterset_class = filters.EmployeeFilter
    ordering_fields = '__all__'
    ordering = ('-id',)

    # def list(self, request, *args, **kwargs):
    #     self.queryset = self.queryset.select_related('marital_status')
    #     return super(EmployeeViewSet, self).list(request, *args, **kwargs)

    # @action(methods=['GET'], detail=False)
    # def get_by_department(self, request, *args, **kwargs):
    #     department = request.query_params.get('department', '')
    #     self.queryset = models.Employee.objects.filter(department__name__icontains=department)
    #     return super(EmployeeViewSet, self).list(request, *args, **kwargs)

    @action(methods=['PATCH'], detail=True)
    def upgrade_salary(self, request, *args, **kwargs):
        result_serializer = serializers_params.UpgradeSalarySerializer(data=request.data)
        result_serializer.is_valid(raise_exception=True)
        employee: 'models.Employee' = self.get_object()
        request.data['salary'] = employee.upgrade_salary(result_serializer.validated_data.get('upgrade_percentage'))
        # behavior_instance = behaviors.BaixaNoEstoqueBehavior(sale='')
        # behavior_instance.run()
        return super(EmployeeViewSet, self).partial_update(request, *args, **kwargs)


class BranchViewSet(viewsets.ModelViewSet):
    queryset = models.Branch.objects.all()
    serializer_class = serializers.BranchSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = models.Department.objects.all()
    serializer_class = serializers.DepartmentSerializer

    @action(methods=['GET'], detail=False)
    def increment_id(self, request, *args, **kwargs):
        queryset = models.Department.objects.increment_id()
        serializer_result = serializers_results.TotalEmployeeSerializer(instance=queryset, many=True)
        return Response(data=serializer_result.data, status=200)

    @action(methods=['GET'], detail=False)
    def total_employee(self, request, *args, **kwargs):
        queryset = models.Department.objects.total_employee()
        return Response(data=queryset, status=200)


class SaleViewSet(viewsets.ModelViewSet):
    queryset = models.Sale.objects.all()
    serializer_class = serializers.SaleSerializer
    # filterset_class = filters.EmployeeFilter
    ordering_fields = '__all__'
    ordering = ('-id',)


class SaleItemViewSet(viewsets.ModelViewSet):
    queryset = models.SaleItem.objects.all()
    serializer_class = serializers.SaleItemSerializer
    filterset_class = filters.SaleItemFilter
    ordering_fields = '__all__'
    ordering = ('-id',)


class DistrictViewSet(viewsets.ModelViewSet):
    queryset = models.District.objects.select_related('city', 'city__state').all()
    serializer_class = serializers.DistrictSerializer
    # filterset_class = filters.SaleItemFilter
    ordering_fields = '__all__'
    ordering = ('-id',)


class CityViewSet(viewsets.ModelViewSet):
    queryset = models.City.objects.all()
    serializer_class = serializers.CitySerializer
    # filterset_class = filters.SaleItemFilter
    ordering_fields = '__all__'
    ordering = ('-id',)


class LongTimeTask(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        serializer_result = serializers_params.LongTimeTaskSerializer(data=request.data)
        serializer_result.is_valid(raise_exception=True)
        tasks.long_time_task.apply_async([serializer_result.validated_data.get('long_time_task')])
        return Response(data={'message': 'O número de loops está sendo gerado'}, status=200)
