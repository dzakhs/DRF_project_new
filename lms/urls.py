from django.urls import path

from lms.apps import LmsConfig
from rest_framework.routers import DefaultRouter

from lms.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, LessonUpdateAPIView, \
    LessonDestroyAPIView, PaymentsListAPIView, SubscriptionCreateAPIView, SubscriptionDeleteAPIView, \
    PaymentsCreateAPIView, PaymentStatus, PaymentsRetrieveAPIView

app_name = LmsConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')





urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lesson/', LessonListAPIView.as_view(), name='lessons'),
    path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-get'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson-delete'),
    path('payment/', PaymentsListAPIView.as_view(), name='payments'),
    path('payment/create/', PaymentsCreateAPIView.as_view(), name='payment-create'),
    path('payment/<int:pk>/check/', PaymentStatus.as_view(), name='payment-status'),
    path('payment/<int:pk>/', PaymentsRetrieveAPIView.as_view(), name='payment-get'),
    path('subscribe/', SubscriptionCreateAPIView.as_view(), name='subscribe-create'),
    path('subscribe/<int:pk>/delete/', SubscriptionDeleteAPIView.as_view(), name='subscribe-delete')

] + router.urls


