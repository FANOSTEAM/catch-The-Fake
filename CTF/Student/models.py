from django.db import models
from EducationAdmin.models import Major,Title

class Certificate(models.Model):
    type_of_certificate=models.CharField(max_length=400)
    profile_picture=models.ImageField()
    firstName=models.CharField(max_length=30,null=False,blank=False)
    middleName=models.CharField(max_length=30,null=False,blank=False)
    lastName=models.CharField(max_length=30,null=False,blank=False)
    CGPA=models.FloatField(null=False,blank=False,default=0.0)
    GPA=models.FloatField(default=0.0)
    title=models.ForeignKey(Title,on_delete=models.CASCADE)
    issued_on=models.DateField()
class Client(models.Model):
    user_name=models.CharField(max_length=30,null=False,blank=False)
    password=models.CharField(max_length=30,null=False,blank=False)
    email=models.EmailField()
    verified=models.BooleanField()
class client_certificate(models.Model):
    client=models.ForeignKey(Client, on_delete=models.CASCADE)
    certificate=models.ForeignKey(Certificate,on_delete=models.CASCADE)
