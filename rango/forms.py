from django import forms
from rango.models import Page, Category, UserProfile
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text="Название для категории")
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	slurl = forms.CharField(widget=forms.HiddenInput(), required=False)
	
	class Meta:
		model = Category
		fields = ("name",)
	
class PageForm(forms.ModelForm):
	title = forms.CharField(max_length=128, help_text="Тут нужно ввести название страницы")
	url = forms.URLField(max_length=200, help_text="Тут должен быть URL страницы")
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	def clean(self):
		cleaned_data = self.cleaned_data
		url = cleaned_data.get('url')
		if url and not url.startswith('http://') and not url.startswith('https://'):
			url = 'http://' + url
			cleaned_data['url'] = url
		return cleaned_data
		
	class Meta:
		model = Page
		exclude = ("category",)
class UserForm(forms.ModelForm):
	repeat_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": 'form-control'}), required=True, max_length=128, min_length=5, help_text="", label="")
	password = forms.CharField(widget=forms.PasswordInput(attrs={"class": 'form-control'}), required=True, max_length=128, min_length=5, label="")
	username = forms.CharField(widget=forms.TextInput(attrs={"class": 'form-control'}), min_length=3, required=True, help_text="", label="")
	email = forms.CharField(widget=forms.TextInput(attrs={"class": 'form-control'}), min_length=3, help_text="", label="")
	class Meta:
		model = User
		fields = {"username", "email", "password"}
		
class UserProfileForm(forms.ModelForm):
	website = forms.CharField(widget=forms.TextInput(attrs={"class": 'form-control'}), help_text="", label="")
	avatar = forms.FileField(widget=forms.FileInput(), required=False, help_text="", label="")
	class Meta:
		model = UserProfile
		fields = {'website', 'avatar'}