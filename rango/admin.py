from django.contrib import admin
from .models import Category, Page
from rango.models import UserProfile

class CatAdm(admin.ModelAdmin):
	prepopulated_fields = {'slurl':('name',)}
	list_display = ('name', 'views', 'likes', 'slurl')
class PageAdm(admin.ModelAdmin):
	prepopulated_fields = {'slurl':('title',)}
	list_display = ('title', 'category', 'slurl')
# Register your models here.
admin.site.register(Page, PageAdm)
admin.site.register(Category, CatAdm)
admin.site.register(UserProfile)