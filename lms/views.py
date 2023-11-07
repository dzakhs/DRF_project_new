
from rest_framework import viewsets, generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny

from lms.paginators import CoursePaginator, LessonPaginator
from lms.permissions import IsOwner, IsModerator
from lms.models import Course, Lesson, Payments, Subscription
from lms.serializers import CourseSerializer, LessonSerializer, PaymentsSerializer, SubscriptionSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]
    pagination_class = CoursePaginator

class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    #permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    pagination_class = LessonPaginator


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    #permission_classes = [IsAuthenticated, IsOwner]
    permission_classes = [AllowAny]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    #permission_classes = [IsAuthenticated, IsModerator | IsOwner]
    permission_classes = [AllowAny]



class LessonUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    #permission_classes = [IsAuthenticated, IsModerator | IsOwner]
    permission_classes = [AllowAny]

class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    #permission_classes = [IsAuthenticated, IsOwner]
    permission_classes = [AllowAny]


class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'payment_method',)
    ordering_fields = ('payment_date',)
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class SubscriptionCreateAPIView(generics.CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def perform_create(self,serializer):
        new_subscription = serializer.save(user=self.request.user)
        new_subscription.user = self.request.user
        new_subscription.is_subscribed = True
        new_subscription.save()


class SubscriptionDeleteAPIView(generics.DestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer