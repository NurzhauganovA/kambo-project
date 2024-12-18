from django.urls import path, include
from foods import views

urlpatterns = [
    path('chef/', views.BestChefsViewSet().as_view(), name='best-chef'),
    path('foods/', views.FoodsApiView.as_view(), name='crete-list-foods'),
    path('foods/<int:pk>/', views.FoodRetrieveUpdateDestroyAPIView.as_view(), name='foods'),
    path('favorites/list/', views.FavoritesViewSet.as_view(), name='favorites'),
    path('favorites/<int:pk>/option/', views.FavoritesOptionViewSet.as_view(), name='favorites-option'),
    path('estimation/', views.EstimationViewSet.as_view(), name='estimation'),
]