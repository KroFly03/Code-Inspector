import os
import subprocess
from typing import Union

from django.core.mail import send_mail
from django.db import transaction

from code_inspector import settings
from users.models import UploadedFile, User, InspectorLog


def get_errors(ex: subprocess.CalledProcessError) -> str:
    lines = ex.stdout.splitlines()

    result = []

    for row in lines:
        if 'FileNotFoundError: [Errno 2] No such file or directory' in row:
            return 'File not found'
        result.append(':'.join(row.split(':')[1:]))

    return '\n'.join(result)


def run_flake8(file_path: str) -> tuple[bool, Union[None, str]]:
    try:
        subprocess.run(['flake8', os.path.join('media', file_path)], check=True, capture_output=True, text=True)
        return True, None
    except subprocess.CalledProcessError as ex:
        return False, get_errors(ex)


def get_logs(files: list[UploadedFile]) -> list[str]:
    results = []

    for file in files:
        file_path = file.file.name

        is_pep8_compliant, pep8_output = run_flake8(file_path)

        file_name = file_path.split('/')[-1]

        if pep8_output == 'File not found':
            results.append(f"Файл {file_name} не найден.\n")
            continue

        if is_pep8_compliant:
            results.append(f"Файл {file_name} успешно проверен по PEP 8.\n")
        else:
            results.append(f"Файл {file_name} не соответствует PEP 8:\n{pep8_output}\n")

        with transaction.atomic():
            file.is_verified = True
            file.save()

            InspectorLog.objects.create(file=file, text=pep8_output, is_pep8_compliant=is_pep8_compliant)

    return results


def send(email: str) -> None:
    user = User.objects.get_by_natural_key(email)

    files = UploadedFile.objects.filter(user=user, is_verified=False).exclude(status=UploadedFile.Status.DELETED)

    if files:
        logs = '\n'.join(get_logs(files))

        send_mail(
            'Результаты проверки файлов',
            logs,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False
        )
