from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.


TYPE = (
    ('Positive', 'Positive'),
    ('Negative' , 'Negative')
    )

class Profile(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    income = models.FloatField(default=0)
    expenses=models.FloatField(default=0)
    balance = models.FloatField(blank=True , null=True,default=0)
    

class Expense(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    amount=models.FloatField(default=0)
    expense_type = models.CharField(max_length=100 , choices=TYPE)
    timestamp = models.DateTimeField(default=datetime.now)

    def __str__(self):
        timestamp_str = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return f"{self.name} ({timestamp_str})"