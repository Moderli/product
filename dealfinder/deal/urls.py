from django.urls import path
from . import views


urlpatterns = [
    path('', views.product_search, name='home'),
    path('signup/', views.signup, name='signup'),
    path('search/', views.product_search, name='product_search'),
    path('logout/', views.custom_logout, name='logout'),
]
