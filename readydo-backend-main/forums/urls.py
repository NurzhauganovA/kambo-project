from django.urls import path, include
from forums import views

urlpatterns = [
    path('forums/', views.ForumAPIView.as_view(), name='get-create-forums'),
    path('forums/message/', views.ForumMessageAPIView.as_view(), name='get-create-message')
]
