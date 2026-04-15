from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('predict/', views.predict, name='predict'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
   path('logout/', views.logout_view, name='logout'),
    path('history/', views.history, name='history'),
    path('english/', views.english, name='english'),
    path('marathi/', views.marathi,name='marathi'),
    path('hindi/', views.hindi,name='hindi'),
]