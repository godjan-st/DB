# Generated by Django 2.1 on 2019-06-11 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0013_auto_20190531_2127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(default='/profile_images/piter.jpg', upload_to='profile_images'),
        ),
    ]
