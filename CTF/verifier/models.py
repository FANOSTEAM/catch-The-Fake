from django.db import models

# Create your models here.
class Employer(models.Model):
    userName=models.CharField(max_length=50,null=False,blank=False,unique=True)
    password=models.CharField(max_length=50,null=False,blank=False)
    email=models.EmailField()
    verified=models.BooleanField()



