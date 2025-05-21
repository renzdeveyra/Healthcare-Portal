from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='portal_home'),
    path('dashboard/', views.dashboard_view, name='portal_dashboard'),
    path('health-profile/', views.health_profile_view, name='health_profile'),
    path('recommendations/', views.recommendations_view, name='recommendations'),
    path('api/update-conditions/', views.update_conditions, name='update_conditions'),
    path('api/recommendations/', views.api_recommendations, name='api_recommendations'),
]
