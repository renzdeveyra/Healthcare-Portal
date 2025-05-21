from django.urls import path
from . import views
from .views import login_view, signup_view, dashboard_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('dashboard/', dashboard_view, name='dashboard'),
]