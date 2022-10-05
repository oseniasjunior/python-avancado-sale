from decimal import Decimal


class EmployeeActions:
    @staticmethod
    def upgrade_salary(employee, upgrade_percentage):
        return round(employee.salary + (employee.salary * (Decimal(upgrade_percentage) / 100)))
