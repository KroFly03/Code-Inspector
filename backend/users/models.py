from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models


class User(AbstractUser):
    username = None
    first_name = models.CharField(verbose_name='Имя', max_length=50)
    last_name = models.CharField(verbose_name='Фамилия', max_length=50)
    email = models.EmailField(verbose_name='Почта', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.set_password(self.password)
        return super().save(*args, **kwargs)


class UploadedFile(models.Model):
    class Status(models.TextChoices):
        NEW = 'new', 'Новый'
        UPDATED = 'updated', 'Обновлен'
        DELETED = 'deleted', 'Удален'

    file = models.FileField(verbose_name='Файл', upload_to='uploads/', validators=[FileExtensionValidator(['.py'])])
    uploaded_at = models.DateTimeField(verbose_name='Загружен', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Обновлен', auto_now=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    status = models.CharField(verbose_name='Статус', choices=Status.choices, default=Status.NEW)

    class Meta:
        verbose_name = 'Загруженный файл'
        verbose_name_plural = 'Загруженные файлы'

    def __str__(self):
        return self.file


class InspectorLog(models.Model):
    text = models.TextField(verbose_name='Текст')
    file = models.ForeignKey(UploadedFile, verbose_name='Файл', on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
