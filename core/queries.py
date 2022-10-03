from core import models
from django.db.models import Sum, Avg, Min, Max, Q, ExpressionWrapper, F, FloatField, Value, Count
from django.db import connection


def questao1():
    qs = models.Employee.objects.filter(
        gender=models.Employee.Gender.FEMALE,
        salary__range=(1000, 5000)
    )
    print(qs.query)
    return qs


def questao2():
    qs = models.Customer.objects.values('name', 'district__name')
    print(qs.query)
    return qs


def questao3():
    qs = models.City.objects.values('name', 'state__abbreviation')
    print(qs.query)
    return qs


def questao4():
    qs = models.Employee.objects.order_by('-salary')[:10]
    print(qs.query)
    return qs


def questao5(marital_status_id: int):
    qs = models.Customer.objects.filter(
        marital_status=marital_status_id
    ).order_by('-income')[:10]
    print(qs.query)
    return qs


def questao6():
    qs = models.Employee.objects.filter(gender=models.Employee.Gender.FEMALE).aggregate(
        total=Sum('salary')
    )
    return qs


def questao7():
    qs = models.Employee.objects.aggregate(
        _sum=Sum('salary'),
        _avg=Avg('salary'),
        _min=Min('salary'),
        _max=Max('salary'),
    )
    return qs


def questao8():
    qs = models.Employee.objects.values('department__name', 'gender').annotate(
        total=Sum('salary')
    ).values('department__name', 'gender', 'total')
    return qs


def questao9():
    qs = models.Employee.objects.aggregate(
        male=Sum('salary', filter=Q(gender=models.Employee.Gender.MALE)),
        female=Sum('salary', filter=Q(gender=models.Employee.Gender.FEMALE))
    )
    return qs


def questao10():
    subtotal = ExpressionWrapper(
        F('saleitem__quantity') * F('saleitem__product__sale_price'),
        output_field=FloatField()
    )
    qs = models.Sale.objects.annotate(
        subtotal=subtotal
    ).values('customer__district__zone__name').annotate(
        total=Sum('subtotal')
    ).filter(date__year__range=(2010, 2015)).annotate(
        zone_name=F('customer__district__zone__name')
    ).values(
        'zone_name',
        'total'
    )
    return qs


def questao11():
    results = []
    sql = """
            SELECT zone.name, SUM((sale_item.quantity * product.sale_price)) AS total
            FROM sale
                     LEFT OUTER JOIN sale_item ON (sale.id = sale_item.id_sale)
                     LEFT OUTER JOIN product ON (sale_item.id_product = product.id)
                     INNER JOIN customer ON (sale.id_customer = customer.id)
                     INNER JOIN district ON (customer.id_district = district.id)
                     INNER JOIN zone ON (district.id_zone = zone.id)
            WHERE EXTRACT('year' FROM sale.date AT TIME ZONE 'UTC') BETWEEN 2010 AND 2015
            GROUP BY zone.name
        """

    with connection.cursor() as cursor:
        cursor.execute(sql)
        results = cursor.fetchall()
    return results


def questao12():
    subtotal = ExpressionWrapper(
        F('saleitem__quantity') * F('saleitem__product__sale_price'),
        output_field=FloatField()
    )
    qs = models.Sale.objects.annotate(
        subtotal=subtotal
    ).values('employee__department__name').annotate(
        total=Sum('subtotal')
    ).filter(date__year__range=(2010, 2015)).values(
        'employee__department__name',
        'total'
    )
    return qs


def questao13():
    subtotal = ExpressionWrapper(
        F('saleitem__quantity') * F('saleitem__product__sale_price'),
        output_field=FloatField()
    )
    qs = models.Sale.objects.annotate(
        subtotal=subtotal,
        commission=ExpressionWrapper(
            F('subtotal') * (F('saleitem__product__product_group__commission_percentage') / Value(100)),
            output_field=FloatField()
        )
    ).values('saleitem__product__product_group__name').annotate(
        total=Sum('commission')
    ).filter(date__year__range=(2010, 2015)).values(
        'saleitem__product__product_group__name',
        'total'
    )
    return qs


def questao14():
    queryset = models.Sale.objects.values('employee__department__name').annotate(
        total=Sum(
            ExpressionWrapper(
                F('saleitem__product__sale_price') * F('saleitem__quantity'), output_field=FloatField()
            )
        )
    ).filter(
        date__year=2010,
        date__month__range=(1, 6)
    ).values('employee__department__name', 'total')
    return queryset


def questao15():
    commission = ExpressionWrapper(
        F('saleitem__product__sale_price') * F('saleitem__quantity') *
        (F('saleitem__product__product_group__commission_percentage') / Value(100)),
        output_field=FloatField()
    )
    queryset = models.Sale.objects.values('saleitem__product__product_group__name').annotate(
        commission=Sum(commission)
    ).filter(
        date__year=2016,
    ).values('saleitem__product__product_group__name', 'commission')
    return queryset


def questao16():
    queryset = models.Customer.objects.values('district__zone__name').annotate(
        quantity=Count('*')
    ).values('district__zone__name', 'quantity')
    return queryset


def questao17():
    queryset = models.City.objects.values('state__name').annotate(
        quantity=Count('*')
    ).values('state__name', 'quantity')
    return queryset
