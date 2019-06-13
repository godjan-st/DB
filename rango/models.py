from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from rango.customsc import rnd_avatar
from random import randint

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	website = models.URLField(blank=True)
	avatar = models.ImageField(upload_to='profile_images', default=rnd_avatar('pushnoy'))
	visits = models.IntegerField(default=0)
	
	def __unicode__(self):
		return self.user.username
	def __str__(self):
		return str(self.user)
	
class Category(models.Model):
	name = models.CharField(max_length=128, unique=True)
	views = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)
	slurl = models.SlugField(unique=True)
	
	def save(self, *args, **kwargs):
		super(Category, self).save(*args, **kwargs)
		
	class Meta:
		verbose_name = "Categories"
		verbose_name_plural = verbose_name
	def __str__(self):
		return self.name
	
class Page(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	title = models.CharField(max_length=128, unique=True, default="1984")
	image = models.ImageField(upload_to="books/", blank=True)
	views = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)
	desc = models.TextField(default="Лучший учебник по построению свободного и прогрессивного государства")
	author = models.CharField(max_length=128, default="Оруелл")
	year = models.CharField(max_length=4, default="1949")
	slurl = models.SlugField(unique=True)
	
	def save(self, *args, **kwargs):
		super(Page, self).save(*args, **kwargs)
	
	class Meta:
		verbose_name = "Pages"
		verbose_name_plural = verbose_name
	def __str__(self):
		return self.title
