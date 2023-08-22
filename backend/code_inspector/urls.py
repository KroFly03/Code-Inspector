from django.urls import path, include

urlpatterns = [
    path('api/auth', include('users.urls.auth')),
    path('api/users', include('users.urls.users')),
]
