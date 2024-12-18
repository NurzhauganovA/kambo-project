from django.urls import path, include
from basket import views

urlpatterns = [
    path('basket/list/', views.BasketUserListAPIView.as_view(), name='basket-list'),
    path('basket/<int:pk>/products-list/', views.BasketProductsListAPIView.as_view(), name='basket-products-list'),
    path('basket/<int:pk>/change-product-quantity/', views.ChangeProductQuantityAPIView.as_view(), name='change-product-quantity'),
    path('basket/food-add/', views.AddToBasketAPIView.as_view(), name='add-to-order'),
    path('basket/<int:pk>/food-remove/', views.RemoveBasketAPIView.as_view(), name='remove-to-order'),
    path('basket/<int:pk>/change-status/', views.BasketChangeStatusAPIView.as_view(), name='basket-change-status'),
]
