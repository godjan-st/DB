from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
	path('about/', views.aboutpage, name='aboutpage'),
	path('randompic/', views.randompic, name='randompic'),
	path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
	path('add_category/', views.add_category, name='add_category'),
	path('page/<slug:page_name_slug>/', views.show_page, name='show_page'),
	path('add_page/', views.add_page, name='add_page'),
	path('register/', views.registration, name='registration'),
	path('login/', views.login, name='login'),
	path("logout/", views.logout_request, name="logout"),
]