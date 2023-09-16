from django.db import models
from EducationAdmin.models import verification
# Create your models here.
class Employer(models.Model):
    username=models.CharField(max_length=50,null=False,blank=False,unique=True)
    password=models.CharField(max_length=50,null=False,blank=False)
    email=models.EmailField()
    owner_tin=models.CharField(max_length=20,null=False,blank=False,default='123456789012',primary_key=True,unique=True)
    code=models.OneToOneField(verification,on_delete=models.CASCADE)
    verified=models.BooleanField()
    def __str__(self):
        return self.username +'===>>'+self.email+f" verified: {self.verified}"



