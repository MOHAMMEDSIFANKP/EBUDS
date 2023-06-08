from django.db import models
from checkout.models import Order
from django.contrib.auth.models import User
# Create your models here.

class Orderreturn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    options = models.CharField(max_length=100,null=True)
    reason = models.TextField(null=True)