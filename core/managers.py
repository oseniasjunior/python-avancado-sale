from django.db.models import Manager, Sum, FloatField, ExpressionWrapper, F


class SaleManager(Manager):
    def total_saled_by_department(self, year: int, start_month: int, end_month: int):
        queryset = self.get_queryset().values('employee__department__name').annotate(
            total=Sum(
                ExpressionWrapper(
                    F('saleitem__product__sale_price') * F('saleitem__quantity'), output_field=FloatField()
                )
            )
        ).filter(
            date__year=year,
            date__month__range=(start_month, end_month)
        ).values('employee__department__name', 'total')
        return queryset


class EmployeeManager(Manager):
    def by_range_salary(self, start_salary, end_salary):
        # TODO: não faça isso para métodos simples
        from core import models as core_models
        return self.get_queryset().filter(
            gender=core_models.Employee.Gender.FEMALE,
            salary__range=(start_salary, end_salary)
        )
