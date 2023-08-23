from django.db import models
from config import settings
from users.models import NULLABLE
class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    image = models.ImageField(upload_to='courses/', verbose_name='превью', **NULLABLE)
    description = models.TextField(verbose_name='описание', **NULLABLE)


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
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.title}'


    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'




class Payments(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь', **NULLABLE)
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='дата оплаты', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='урок', **NULLABLE)
    amount = models.IntegerField(verbose_name='сумма', **NULLABLE)
    payment_method = models.CharField(max_length=150, verbose_name='способ оплаты', **NULLABLE)


    def __str__(self):
        return f'{self.course}, {self.lesson}, {self.payment_method}, {self.amount}'



    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'