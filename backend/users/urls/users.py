from django.urls import path

from users.views import UserCreateView, UserDetailView, FileView, FileDetailVIew

app_name = 'users'

urlpatterns = [
    path('', UserCreateView.as_view(), name='users-user'),
    path('/me', UserDetailView.as_view(), name='users-me'),
    path('/me/files', FileView.as_view(), name='users-files'),
    path('/me/files/<int:pk>', FileDetailVIew.as_view(), name='users-files-detail')
]
