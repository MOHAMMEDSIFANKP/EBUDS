from django.db import models
from product.models import Product
from checkout.models import Order
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Coupon(models.Model):
    coupon_code = models.CharField(max_length=50, unique=True)
    discount = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(30)])
    min_value = models.IntegerField(validators=[MinValueValidator(0)])
    valid_from = models.DateField(auto_now_add=True)
    valid_till = models.DateField()
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.coupon_code
    
class Usercoupon(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon,on_delete=models.CASCADE)
    used = models.BooleanField(default=False)
    total_price = models.BigIntegerField()


    