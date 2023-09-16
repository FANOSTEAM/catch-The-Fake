from django.db import models
from EducationAdmin.models import Title,Collage
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from django.db.models.signals import post_delete

image_storage = FileSystemStorage(
    # Physical file location ROOT
    location=u'{0}/student_profiles/'.format(settings.MEDIA_ROOT),
    # Url for file
    base_url=u'{0}student_profiles/'.format(settings.MEDIA_URL),
)


def image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/my_sell/picture/<filename>
    return u'{2}/{0}/{1}'.format(instance.firstName + "_"+ instance.middleName+"_"+instance.lastName,filename,instance.issued_on.year)

class Certificate(models.Model):

    school=models.ForeignKey(Collage,on_delete=models.CASCADE)
    type_of_certificate=models.CharField(max_length=400)
    profile_picture=models.ImageField(upload_to=image_directory_path, storage=image_storage)
    firstName=models.CharField(max_length=30,null=False,blank=False)
    middleName=models.CharField(max_length=30,null=False,blank=False)
    lastName=models.CharField(max_length=30,null=False,blank=False)
    CGPA=models.FloatField(null=False,blank=False,default=0.0)
    GPA=models.FloatField(default=0.0)
    title=models.ForeignKey(Title,on_delete=models.CASCADE)
    ban=models.BooleanField(default=True)
    issued_on=models.DateField()
    def __str__(self):
        return self.type_of_certificate
class Client(models.Model):
    user_name=models.CharField(max_length=30,null=False,blank=False,unique=True)
    password=models.CharField(max_length=30,null=False,blank=False)
    email=models.EmailField()
    verified=models.BooleanField()
    def __str__(self):
        return self.username+'===>>'+self.email+f' verified{self.verified}'
class client_certificate(models.Model):
    client=models.ForeignKey(Client, on_delete=models.CASCADE)
    certificate=models.ForeignKey(Certificate,on_delete=models.CASCADE)
    def __str__(self):
        return self.client.user_name+'===>>'+self.certificate.title


