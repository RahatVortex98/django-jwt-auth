from django.urls import path
from .views import RegisterView, VerifyEmailView ,CustomTokenObtainPairView,LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/<uidb64>/<token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
     path('api/logout/', LogoutView.as_view(), name='logout'),
]
