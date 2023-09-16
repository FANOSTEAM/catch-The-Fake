from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage                                                               

image_storage = FileSystemStorage(
    # Physical file location ROOT
    location=u'{0}/'.format(settings.MEDIA_ROOT),
    # Url for file
    base_url=u'{0}'.format(settings.MEDIA_URL),
)



def image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/my_sell/picture/<filename>
    return u'{0}'.format(filename)

class verification(models.Model):
    creation_date=models.DateTimeField()
    expiration_date=models.DateTimeField()
    code=models.IntegerField()
    def __str__(self):
        return 'Expiration time:' + str(self.expiration_date)

class University(models.Model):
    name=models.CharField(max_length=100,null=False, blank=False,unique=True)
    logo=models.ImageField(upload_to=image_directory_path ,storage=image_storage)
    UniversityId=models.CharField(unique=True,max_length=50,null=False,blank=False)
    user_name=models.CharField(unique=True,max_length=50,null=False,blank=False)
    password=models.CharField(max_length=50,null=False,blank=False)
    def __str__(self):
        return self.name
class Collage(models.Model):
    university=models.ForeignKey(University,on_delete=models.CASCADE)
    name=models.CharField(max_length=200,null=False,blank=False,default="unknown")
class Major(models.Model):
    collage=models.ForeignKey(Collage,on_delete=models.CASCADE)
    name=models.CharField(max_length=70,)
    def __str__(self):
        return str(self.collage)+'===>>'+self.name

class Title(models.Model):
    major=models.ForeignKey(Major,on_delete=models.CASCADE)
    title=models.CharField(max_length=80,null=False,blank=False)
    def __str__(self):
        return self.major.name +'===>>'+self.title
class AdminUser(models.Model):
    Name=models.CharField(max_length=40,null=False,blank=False)
    userName=models.CharField(max_length=50,null=False, blank=False,unique=True)
    password=models.CharField(max_length=50,null=False, blank=False)
    email=models.EmailField()
    verified=models.BooleanField()
    code=models.ManyToManyField(verification,)
    def __str__(self):
        return self.Name+'===>>'+self.email+ f" verified: {self.verified}"




