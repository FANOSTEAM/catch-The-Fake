from django.db import models
class verification(models.Model):
    creation_date=models.DateTimeField()
    expiration_date=models.DateTimeField()
    code=models.IntegerField()
class University(models.Model):
    name=models.CharField(max_length=100,null=False, blank=False)
    logo=models.ImageField()
    user_name=models.CharField(unique=True,max_length=50,null=False,blank=False)
    password=models.CharField(unique=True,max_length=50,null=False,blank=False)

class Major(models.Model):
    university=models.ForeignKey(University,on_delete=models.CASCADE)
    name=models.CharField(max_length=20,null=False)
class Title(models.Model):
    major=models.ForeignKey(Major,on_delete=models.CASCADE)
    title=models.CharField(max_length=80,null=False,blank=False)

class AdminUser(models.Model):
    Name=models.CharField(max_length=40,null=False,blank=False)
    userName=models.CharField(max_length=50,null=False, blank=False,unique=True)
    password=models.CharField(max_length=50,null=False, blank=False)
    email=models.EmailField()
    verified=models.BooleanField()
