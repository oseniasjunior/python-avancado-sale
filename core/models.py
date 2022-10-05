from decimal import Decimal

from django.db import models
from core import managers


# Create your models here.
class ModelBase(models.Model):
    id = models.AutoField(
        primary_key=True,
        null=False
    )
    active = models.BooleanField(
        null=False,
        default=True
    )
    created_at = models.DateTimeField(
        null=False,
        auto_now_add=True
    )
    modified_at = models.DateTimeField(
        null=False,
        auto_now=True
    )

    class Meta:
        abstract = True
        managed = True


class Department(ModelBase):
    name = models.CharField(
        null=False,
        max_length=64,
        unique=True
    )

    objects = managers.DepartmentManager()

    class Meta:
        db_table = 'department'


class MaritalStatus(ModelBase):
    name = models.CharField(
        null=False,
        max_length=64,
        unique=True
    )

    class Meta:
        db_table = 'marital_status'


class Supplier(ModelBase):
    name = models.CharField(
        null=False,
        max_length=64,
    )
    legal_document = models.CharField(
        null=False,
        max_length=20,
        unique=True
    )

    class Meta:
        db_table = 'supplier'


class ProductGroup(ModelBase):
    name = models.CharField(
        null=False,
        max_length=64,
        unique=True
    )
    commission_percentage = models.DecimalField(
        null=False,
        max_digits=5,
        decimal_places=2
    )
    gain_percentage = models.DecimalField(
        null=False,
        max_digits=5,
        decimal_places=2
    )

    class Meta:
        db_table = 'product_group'


class State(ModelBase):
    name = models.CharField(
        null=False,
        max_length=64,
        unique=True
    )
    abbreviation = models.CharField(
        null=False,
        max_length=2,
        unique=True
    )

    class Meta:
        db_table = 'state'


class City(ModelBase):
    name = models.CharField(
        null=False,
        max_length=64
    )
    state = models.ForeignKey(
        to='State',
        on_delete=models.DO_NOTHING,
        null=False,
        db_column='id_state'
    )

    class Meta:
        db_table = 'city'
        unique_together = [
            ('name', 'state',)
        ]


class Zone(ModelBase):
    name = models.CharField(
        null=False,
        max_length=64,
        unique=True
    )

    class Meta:
        db_table = 'zone'


class District(ModelBase):
    name = models.CharField(
        null=False,
        max_length=64
    )
    city = models.ForeignKey(
        to='City',
        on_delete=models.DO_NOTHING,
        null=False,
        db_column='id_city'
    )
    zone = models.ForeignKey(
        to='Zone',
        on_delete=models.DO_NOTHING,
        null=False,
        db_column='id_zone'
    )

    class Meta:
        db_table = 'district'
        unique_together = [
            ('name', 'city', 'zone',)
        ]


class Branch(ModelBase):
    name = models.CharField(
        null=False,
        max_length=64,
        unique=True
    )
    district = models.ForeignKey(
        to='District',
        on_delete=models.DO_NOTHING,
        null=False,
        db_column='id_district'
    )

    class Meta:
        db_table = 'branch'


class Customer(ModelBase):
    class Gender(models.TextChoices):
        FEMALE = 'F', 'Female'
        MALE = 'M', 'Male'

    name = models.CharField(
        null=False,
        max_length=64,
    )
    district = models.ForeignKey(
        to='District',
        on_delete=models.DO_NOTHING,
        null=False,
        db_column='id_district'
    )
    marital_status = models.ForeignKey(
        to='MaritalStatus',
        on_delete=models.DO_NOTHING,
        null=False,
        db_column='id_marital_status'
    )
    income = models.DecimalField(
        null=False,
        max_digits=16,
        decimal_places=2
    )
    gender = models.CharField(
        null=False,
        max_length=1,
        choices=Gender.choices
    )

    class Meta:
        db_table = 'customer'


class Employee(ModelBase):
    class Gender(models.TextChoices):
        FEMALE = 'F', 'Female'
        MALE = 'M', 'Male'

    name = models.CharField(
        null=False,
        max_length=64,
    )
    district = models.ForeignKey(
        to='District',
        on_delete=models.DO_NOTHING,
        null=False,
        db_column='id_district'
    )
    marital_status = models.ForeignKey(
        to='MaritalStatus',
        on_delete=models.DO_NOTHING,
        null=False,
        db_column='id_marital_status'
    )
    department = models.ForeignKey(
        to='Department',
        on_delete=models.DO_NOTHING,
        null=False,
        db_column='id_department'
    )
    salary = models.DecimalField(
        null=False,
        max_digits=16,
        decimal_places=2
    )
    admission_date = models.DateField(
        null=False
    )
    birth_date = models.DateField(
        null=False
    )
    gender = models.CharField(
        null=False,
        max_length=1,
        choices=Gender.choices
    )
    objects = models.Manager()
    queries = managers.EmployeeManager()

    class Meta:
        db_table = 'employee'

    def upgrade_salary(self, upgrade_percentage):
        return round(self.salary + (self.salary * (Decimal(upgrade_percentage) / 100)))


class Product(ModelBase):
    name = models.CharField(
        null=False,
        max_length=64,
        unique=True
    )
    product_group = models.ForeignKey(
        to='ProductGroup',
        on_delete=models.DO_NOTHING,
        null=False,
        db_column='id_product_group'
    )
    supplier = models.ForeignKey(
        to='Supplier',
        on_delete=models.DO_NOTHING,
        null=False,
        db_column='id_supplier'
    )
    cost_price = models.DecimalField(
        null=False,
        max_digits=16,
        decimal_places=2
    )
    sale_price = models.DecimalField(
        null=False,
        max_digits=16,
        decimal_places=2
    )

    class Meta:
        db_table = 'product'


class Sale(ModelBase):
    customer = models.ForeignKey(
        to='Customer',
        on_delete=models.DO_NOTHING,
        null=False,
        db_column='id_customer'
    )
    branch = models.ForeignKey(
        to='Branch',
        on_delete=models.DO_NOTHING,
        null=False,
        db_column='id_branch'
    )
    employee = models.ForeignKey(
        to='Employee',
        on_delete=models.DO_NOTHING,
        null=False,
        db_column='id_employee'
    )
    date = models.DateTimeField(
        null=False,
        auto_now_add=True
    )
    objects = managers.SaleManager()

    class Meta:
        db_table = 'sale'


class SaleItem(ModelBase):
    sale = models.ForeignKey(
        to='Sale',
        on_delete=models.DO_NOTHING,
        null=False,
        db_column='id_sale'
    )
    product = models.ForeignKey(
        to='Product',
        on_delete=models.DO_NOTHING,
        null=False,
        db_column='id_product'
    )
    quantity = models.DecimalField(
        null=False,
        max_digits=16,
        decimal_places=3
    )

    class Meta:
        db_table = 'sale_item'
