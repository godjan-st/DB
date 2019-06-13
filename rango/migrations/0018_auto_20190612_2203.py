# Generated by Django 2.1 on 2019-06-12 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0017_auto_20190612_2156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='slurl',
            field=models.SlugField(unique=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(default='/profile_images/push.jpg', upload_to='profile_images'),
        ),
    ]
