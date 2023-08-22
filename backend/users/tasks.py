from code_inspector.celery import app
from users.models import User
from users.services import send


@app.task
def send_report():
    for user in User.objects.filter(is_active=True):
        send(user.email)
