from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from users.models import User, UploadedFile, InspectorLog
from users.serializers import UserSerializer, FileSerializer, FileInspectorSerializer


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    authentication_classes = []


class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class BaseFileView(GenericAPIView):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UploadedFile.objects.filter(user=self.request.user)


class FileView(generics.ListCreateAPIView, BaseFileView):
    pass


class FileDetailView(generics.RetrieveUpdateDestroyAPIView, BaseFileView):
    http_method_names = ['get', 'put', 'delete']

    def perform_destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.serializer_class()
        serializer.delete(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)


class FileInspectorView(generics.ListAPIView):
    serializer_class = FileInspectorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        file_id = self.kwargs.get('pk')
        return InspectorLog.objects.filter(file__user=self.request.user, file_id=file_id).order_by('-created_at')
