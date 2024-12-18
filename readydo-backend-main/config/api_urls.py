from django.urls import path, include

urlpatterns = [
    path('', include('auth_user.urls')),
    path('', include('foods.urls')),
    path('', include('basket.urls')),
    path('', include('forums.urls')),
]
