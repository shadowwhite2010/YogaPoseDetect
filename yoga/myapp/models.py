from django.db import models

# Create your models here.

class Image(models.Model):
    # title = models.CharField(max_length=200, default="some_image")
    image = models.ImageField(upload_to='images')