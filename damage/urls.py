from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('detection/<int:claim>/', views.detection, name='detection'),
    path('result/', views.result, name='result'),
    path('check_file/<str:claim>/', views.check_file, name='check_file'),
    path('login/', views.user_login, name='login'),
    path('adminlogin/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('claims/', views.claims, name='claims'),
    url(r'^individualclaim/(?P<claim>[0-9]+)/$', views.individualclaim, name='individualclaim'),
    path('individuals_claims_from_superuser/<str:individual>/', views.individuals_claims_from_superuser, name='individualsclaims'),
    path('download/<int:claim>/', views.download, name='download'),
]

