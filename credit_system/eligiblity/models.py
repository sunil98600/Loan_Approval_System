from django.db import models

# Create your models here.
class Customer(models.Model):
    customer_id= models.IntegerField(default=0)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.IntegerField()
    monthly_salary = models.IntegerField()
    approved_limit = models.IntegerField()
    #current_debt = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
      return "%s %s " %(self.first_name , self.last_name)

class Loan(models.Model):
    customer_id= models.ForeignKey(Customer, on_delete=models.CASCADE)
    loan_amount = models.IntegerField()
    tenure = models.IntegerField()
    interest_rate = models.IntegerField()
    monthly_repayment = models.ImageField()
    emis_paid_on_time = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
