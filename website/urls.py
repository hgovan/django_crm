from django.urls import path
from . import views
# from django.conf.urls import handler404

urlpatterns = [
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('verify/', views.verify_code, name='verify_code'),
]

# handler404 = views.custom_404_page
