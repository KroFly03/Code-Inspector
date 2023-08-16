from rest_framework import generics, views, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from users.models import User, UploadedFile
from users.serializers import UserSerializer, FileSerializer


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    authentication_classes = []


class UserDetailView(views.APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)


class BaseFileView(GenericAPIView):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UploadedFile.objects.filter(user=self.request.user)


class FileView(generics.ListCreateAPIView, BaseFileView):
    pass


class FileDetailVIew(generics.RetrieveUpdateDestroyAPIView, BaseFileView):
    http_method_names = ['get', 'put', 'delete']

    def perform_destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.serializer_class()
        serializer.delete(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)
