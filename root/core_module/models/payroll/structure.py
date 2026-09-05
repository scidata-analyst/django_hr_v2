from django.db import models


class SalaryStructure(models.Model):
    structure_name = models.CharField(max_length=100, unique=True)
    grade_level = models.CharField(max_length=20, blank=True)
    basic_salary = models.DecimalField(max_digits=12, decimal_places=2)
    house_rent_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    transport_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    medical_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    food_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    income_tax_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    provident_fund_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    insurance_premium = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['structure_name']

    def __str__(self):
        return self.structure_name

    @property
    def gross_salary(self):
        house_rent = (self.basic_salary * self.house_rent_percent) / 100
        return self.basic_salary + house_rent + self.transport_allowance + \
               self.medical_allowance + self.food_allowance + self.other_allowance

    @property
    def total_deductions(self):
        house_rent = (self.basic_salary * self.house_rent_percent) / 100
        gross = self.basic_salary + house_rent + self.transport_allowance + \
                self.medical_allowance + self.food_allowance + self.other_allowance
        tax = (gross * self.income_tax_percent) / 100
        pf = (self.basic_salary * self.provident_fund_percent) / 100
        return tax + pf + self.insurance_premium + self.other_deductions

    @property
    def net_salary(self):
        return self.gross_salary - self.total_deductions
