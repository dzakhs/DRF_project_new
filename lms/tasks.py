from celery import shared_task
from django.core.mail import send_mail
from config import settings
from lms.models import Subscription

@shared_task
def send_course_update(course_pk):
    course_list = Subscription.objects.filter(course_id=course_pk)
    for item in course_list:
        send_mail(
            subject=f'Обновление курса {item.course.title}',
            message=f'Обновление курса {item.course.title}',
            recipient_list=[item.user.email],
            from_email=settings.EMAIL_HOST_USER
        )
        print('Сообщение отправлено!')