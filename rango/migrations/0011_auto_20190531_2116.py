# Generated by Django 2.1 on 2019-05-31 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0010_auto_20190531_2106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(default='/profile_images/maxresdefault.jpg', upload_to='profile_images'),
        ),
    ]
