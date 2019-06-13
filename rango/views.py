from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from os.path import isfile, join
from os import listdir
from django.conf import settings
from random import randint
from rango.models import Category, Page, User, UserProfile
from rango.forms import CategoryForm,PageForm,UserForm,UserProfileForm
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
import time
def index(request):
		piter = "piter.jpg"
		category_list = Category.objects.order_by('name')
		page_list = Page.objects.order_by('views')[:8]
		context_dict = {'boldmessage': "This is zhirniy text",
						'mainpic': piter,
						'categories': category_list,
						'pages': page_list}
		if request.user.is_authenticated:
			name = request.user
			current_user = UserProfile.objects.get(user=name)
			visits = current_user.visits
			request.session['visits'] = visits
			if 'last_visit' in request.session:
				last_visit = request.session['last_visit']
				last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
				if (datetime.now() - last_visit_time) > timedelta(days=1):
					request.session['visits']= visits+1
					request.session['last_visit']=str(datetime.now())
				print (last_visit_time)
			else:
				request.session['last_visit']=str(datetime.now())
				request.session['visits']= visits+1
			current_user.visits = request.session['visits']
			current_user.save()
			visits = request.session['visits']
			context_dict['visits']=visits
		return render(request, "rango/index.html", context_dict)
def aboutpage(request):
	context_dict={}
	if request.user.is_authenticated:
		name = request.user
		current_user = UserProfile.objects.get(user=name)
		visits = current_user.visits
		context_dict['visits']=visits
	else:
		context_dict['visits']=0
	category_list = Category.objects.order_by('name')
	context_dict['categories']=category_list
	return render(request, "rango/about.html", context_dict)
def randompic(request):
		pictures = [f for f in listdir(settings.STATIC_PATH) if isfile(join(settings.STATIC_PATH, f))]
		key = randint(0, (len(pictures)-1))
		randpic = pictures[key]
		context_dict = {'boldmessage': "RANDOM PICTURE!",
						'randpic': randpic}
		if request.user.is_authenticated:
			name = request.user
			current_user = UserProfile.objects.get(user=name)
			visits = current_user.visits
			context_dict['visits']=visits
		else:
			context_dict['visits']=0
		category_list = Category.objects.order_by('name')
		context_dict['categories']=category_list
		return render(request, "rango/randompic.html", context_dict)
def show_category(request, category_name_slug):
	context_dict = {}
	try:
		category = Category.objects.get(slurl=category_name_slug)
		pages = Page.objects.filter(category=category)
		context_dict['pages'] = pages
		context_dict['category'] = category 
	except Category.DoesNotExist:
		context_dict['pages'] = None
		context_dict['category'] = None
	if request.user.is_authenticated:
		name = request.user
		current_user = UserProfile.objects.get(user=name)
		visits = current_user.visits
		context_dict['visits']=visits
	else:
		context_dict['visits'] = None
	category_list = Category.objects.order_by('name')
	context_dict['categories']=category_list
	return render(request, "rango/category.html", context_dict)
	
def show_page(request, page_name_slug):
	context_dict = {}
	try:
		page = Page.objects.get(slurl=page_name_slug)
		context_dict['page'] = page
		page.views+=1
	except Category.DoesNotExist:
		context_dict['page'] = None	
	if request.user.is_authenticated:
		name = request.user
		current_user = UserProfile.objects.get(user=name)
		visits = current_user.visits
		context_dict['visits']=visits
	else:
		context_dict['visits']=0
	category_list = Category.objects.order_by('name')
	context_dict['categories']=category_list
	return render(request, "rango/show_page.html", context_dict)
	
@login_required
def add_category(request):
	form = CategoryForm()
	
	if request.method == "POST":
		form = CategoryForm(request.POST)
		
		if form.is_valid():
			cat = form.save(commit=True)
			return index(request)
		else:
			print(form.errors)
	
	return render(request, "rango/add_category.html", {'form':form})

@login_required
def add_page(request, category_name_slug):
	try:
		category = Category.objects.get(slurl=category_name_slug)
	except Category.DoesNotExist:
		category = None
	form = PageForm()
	if request.method == 'POST':
		form = PageForm(request.POST)
		if form.is_valid():
			if category:
				page = form.save(commit=False)
				page.category = category
				page.views = 0
				page.save()
				return show_category(request, category_name_slug)
		else:
			print(form.errors)
	context_dict = {'form':form, 'category': category}
	return render(request, 'rango/add_page.html/', context_dict)
	
def registration(request):
	registered = False
	if request.method == 'POST':
		user_form = UserForm(request.POST)
		profile_form = UserProfileForm(request.POST)
		if user_form.is_valid() and profile_form.is_valid():
			if user_form.cleaned_data['password'] == user_form.cleaned_data['repeat_password']:
				user = user_form.save()
				user.set_password(user.password)
				user.save()
				profile = profile_form.save(commit=False)
				profile.user = user
				if 'avatar' in request.FILES:
					profile.avatar = request.FILES['avatar']
				profile.save()
				registered = True
				result = "Пользователь создан успешно."
			else:
				result = "Пароли не совпадают"
		else:
			result = user_form.errors, profile_form.errors
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()
		result = ""
	context_dict = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered, 'result': result,
	'user_pic': 'user_pic.jpg'}
	return render(request, 'rango/register.html', context_dict)

def login(request):
	context_dict = {}
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				auth_login(request, user)
				return HttpResponseRedirect('/rango/')
			else:
				context_dict = {'result': 'пользователь неактивен'}
				return render(request, 'rango/login.html', context_dict)
		else:
			context_dict = {'result': 'неправильно введены данные'}
			return render(request, 'rango/login.html', context_dict)
	else:
		return render(request, 'rango/login.html', context_dict)

@login_required
def logout_request(request):
	logout(request)
	return HttpResponseRedirect('/rango/')