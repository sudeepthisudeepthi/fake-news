from django.db import models


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phno = models.BigIntegerField()
    password = models.CharField(max_length=100)
    address = models.TextField()
    pincode = models.IntegerField()

    class Meta:
        db_table = "user"


class Admin(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    class Meta:
        db_table = "admin"


class News(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.FileField()
    date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "news"
