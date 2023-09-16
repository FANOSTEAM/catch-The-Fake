from django.db import models


class Organization(models.Model):
    OwnerTIN=models.CharField(max_length=20,null=False,blank=False,unique=True)
    LicenceNumber=models.CharField(max_length=30,null=False,blank=False,unique=True)
    phone=models.CharField(max_length=13)



