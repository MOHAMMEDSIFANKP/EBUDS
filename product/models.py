from django.db import models
from django.urls import reverse
from dashboard.models import brand
from category.models import category
from django.utils.text import slugify

# Create your models here.

# Color
class Color(models.Model):
    color = models.CharField(max_length=100)

    def __str__(self):
        return self.color
# Price Filter
class PriceFilter(models.Model):
    FILTER_CHOICES = (
        ('100 TO 1000', '100 TO 1000'),
        ('1000 TO 10000', '1000 TO 10000'),
        ('10000 TO 20000', '10000 TO 20000'),
        ('20000 TO 30000', '20000 TO 30000'),
        ('30000 TO 40000', '30000 TO 40000'),
        ('40000 TO 50000', '40000 TO 50000'),
        ('50000 and above', '50000 and above'),
    )
    price_range = models.CharField(choices=FILTER_CHOICES, max_length=60)
    
    def __str__(self):
        return self.price_range
# Offer
class Offer(models.Model):
    offer_name = models.CharField(max_length=100)
    discount_amount = models.PositiveIntegerField()
    
    def _str_(self):
        return self.offer_name

# product
class Product(models.Model):
    product_name = models.CharField(unique=True,max_length=50)
    product_price = models.IntegerField()
    price_range = models.ForeignKey(PriceFilter, on_delete=models.CASCADE)
    brand = models.ForeignKey(brand,on_delete=models.CASCADE)
    category = models.ForeignKey(category,on_delete=models.CASCADE)
    product_description = models.TextField(blank=True)
    offer = models.ForeignKey(Offer, on_delete=models.SET_NULL, null=True )
    is_available = models.BooleanField(default=False)
    slug = models.SlugField(max_length=250,unique=True)

    def save(self, *args, **kwargs):
        # generate slug field from name field if slug is empty
        if not self.slug:
            self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)

    def get_url(self):
        return reverse('single',args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name
    def get_offer(self):
        return self.product_price - self.offer.discount_amount


# Variations
class Variations(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    image1 = models.ImageField(upload_to='photos/variations')
    image2 = models.ImageField(upload_to='photos/variations')
    image3 = models.ImageField(upload_to='photos/variations')


    
