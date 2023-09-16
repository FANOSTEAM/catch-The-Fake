# Generated by Django 4.2.4 on 2023-09-09 07:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('EducationAdmin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employer',
            fields=[
                ('username', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('owner_tin', models.CharField(default='123456789012', max_length=20, primary_key=True, serialize=False, unique=True)),
                ('verified', models.BooleanField()),
                ('code', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='EducationAdmin.verification')),
            ],
        ),
    ]
