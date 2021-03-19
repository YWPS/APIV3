from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=256)
    code1name = models.CharField(max_length=256)
    code2name = models.CharField(max_length=256)
    code3name = models.CharField(max_length=256)
    code1code = models.CharField(max_length=256)
    code2code = models.CharField(max_length=256)
    code3code = models.CharField(max_length=256)
    hash = models.CharField(max_length=45)
    user = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.name}"


class Image(models.Model):
    name = models.CharField(max_length=256)
    extension = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}.{self.extension}"
