from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'auth'

urlpatterns = [
    path('/token', TokenObtainPairView.as_view(), name='token'),
    path('/refresh', TokenRefreshView.as_view(), name='refresh'),
]