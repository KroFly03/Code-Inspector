from django.urls import path

from users.views import UserCreateView, UserDetailView, FileView, FileDetailView, FileInspectorView

app_name = 'users'

urlpatterns = [
    path('', UserCreateView.as_view(), name='users-user'),
    path('/me', UserDetailView.as_view(), name='users-me'),
    path('/me/files', FileView.as_view(), name='users-files'),
    path('/me/files/<int:pk>', FileDetailView.as_view(), name='users-files-detail'),
    path('/me/files/<int:pk>/logs', FileInspectorView.as_view(), name='users-files-detail-log'),
]
