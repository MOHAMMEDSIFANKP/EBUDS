from django.db import models


 
class GeeksModel(models.Model):
    name = models.CharField(max_length = 200)
    photo = models.ImageField(upload_to='photos/variations')
    price = models.IntegerField()
    description = models.TextField()

 
    def __str__(self):
        return self.name