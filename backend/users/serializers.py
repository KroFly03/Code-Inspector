from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import User, UploadedFile, InspectorLog


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = (
            'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'groups', 'user_permissions'),


class FileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UploadedFile
        fields = '__all__'
        read_only_fields = ('id', 'status', 'uploaded_at', 'updated_at', 'user')

    def update(self, instance: UploadedFile, validated_data):
        if instance.status == UploadedFile.Status.DELETED:
            raise ValidationError({'file': ['Данный файл уже удален.']})

        instance.status = UploadedFile.Status.UPDATED
        instance.is_verified = False
        instance.save()
        return super().update(instance, validated_data)

    def delete(self, instance: UploadedFile):
        if instance.status == UploadedFile.Status.DELETED:
            raise ValidationError({'file': ['Данный файл уже удален.']})

        instance.status = UploadedFile.Status.DELETED
        instance.save()


class FileInspectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspectorLog
        exclude = ('id', 'file')
