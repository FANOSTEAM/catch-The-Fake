# Generated by Django 4.2.4 on 2023-09-09 07:09

import Student.models
import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('EducationAdmin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of_certificate', models.CharField(max_length=400)),
                ('profile_picture', models.ImageField(storage=django.core.files.storage.FileSystemStorage(base_url='/media/student_profiles/', location='C:\\Users\\KODE\\CTF\\CTF\\media/student_profiles/'), upload_to=Student.models.image_directory_path)),
                ('firstName', models.CharField(max_length=30)),
                ('middleName', models.CharField(max_length=30)),
                ('lastName', models.CharField(max_length=30)),
                ('CGPA', models.FloatField(default=0.0)),
                ('GPA', models.FloatField(default=0.0)),
                ('ban', models.BooleanField(default=True)),
                ('issued_on', models.DateField()),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EducationAdmin.collage')),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EducationAdmin.title')),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=30, unique=True)),
                ('password', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('verified', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='client_certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('certificate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Student.certificate')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Student.client')),
            ],
        ),
    ]
