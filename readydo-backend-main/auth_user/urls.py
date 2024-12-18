from django.urls import path, include
from auth_user import views

urlpatterns = [
    path('auth/token/', views.CustomTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('auth/token/refresh/', views.CustomTokenRefreshView.as_view(), name='token-refresh'),
    path('auth/register/', views.RegisterApi.as_view({'post': 'post'}), name='register'),
    path('auth/password-reset-send-code/', views.PasswordResetCodeRequestApi.as_view(),
         name='password-reset-request'),
    path('auth/password-varify-code/', views.PasswordResetVarifyCodeAPIView.as_view({'post': 'post'}),
         name='password-reset-varify'),

    path('user-profile/', views.UserProfileView.as_view({'get': 'get', 'patch': 'update'}), name='user-profile'),
    path('friends/', views.FriendsView.as_view(), name='friends'),
]
