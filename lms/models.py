from django.db import models
from config import settings
from users.models import NULLABLE
class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    image = models.ImageField(upload_to='courses/', verbose_name='превью', **NULLABLE)
    description = models.TextField(verbose_name='описание', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь', **NULLABLE)


    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'



class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание', **NULLABLE)
    image = models.ImageField(upload_to='lessons/', verbose_name='превью', **NULLABLE)
    url = models.URLField(verbose_name='ссылка', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь', **NULLABLE)

    def __str__(self):
        return f'{self.title}'


    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'




class Payments(models.Model):

    payment_choices = [
        ('cash', 'Наличные'),
        ('credit_card', 'Оплата картой')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь', **NULLABLE)
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='дата оплаты', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='урок', **NULLABLE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='сумма', **NULLABLE)
    payment_method = models.CharField(max_length=150, choices=payment_choices, verbose_name='способ оплаты', **NULLABLE)
    payment_status = models.BooleanField(default=False, verbose_name='статус оплаты')
    payment_url = models.URLField(verbose_name='Ссылка на оплату картой', **NULLABLE)
    payment_id = models.CharField(max_length=50, verbose_name='id платежа', **NULLABLE)
    def __str__(self):
        return f'{self.course}, {self.lesson}, {self.payment_method}, {self.amount}'



    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')
    is_subscribed = models.BooleanField(default=False, verbose_name='признак подписки')


    def __str__(self):
        return f'{self.user} - {self.course.title}'

    class Meta:
        verbose_name = 'Подписка на курс'
        verbose_name_plural = 'Подписки на курсы'