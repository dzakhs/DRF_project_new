import stripe
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from config import settings
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
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    pagination_class = LessonPaginator


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    # permission_classes = [IsAuthenticated, IsOwner]
    permission_classes = [AllowAny]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    # permission_classes = [IsAuthenticated, IsModerator | IsOwner]
    permission_classes = [AllowAny]


class LessonUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    # permission_classes = [IsAuthenticated, IsModerator | IsOwner]
    permission_classes = [AllowAny]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    # permission_classes = [IsAuthenticated, IsOwner]
    permission_classes = [AllowAny]


class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'payment_method',)
    ordering_fields = ('payment_date',)
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class PaymentsCreateAPIView(generics.CreateAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer

    def perform_create(self, serializer):
        try:
            data = serializer.save(user=self.request.user)
            name = data.course
            unit_amount = data.course.price
            stripe.api_key = settings.STRIPE_SECRET_KEY
            product = stripe.Product.create(name=name)
            data_product = product.id
            amount = stripe.Price.create(
                unit_amount=int(unit_amount) * 100,
                currency='rub',
                product=data_product,
            )
            data_price = amount.id
            url_pay = stripe.checkout.Session.create(
                success_url='https://example.com/success',
                line_items=[
                    {
                        'price': data_price,
                        'quantity': 1,
                    }

                ],
                mode='payment'
            )
            data.user = self.request.user
            data.payment_url = url_pay.url
            data.payment = int(amount.unit_amount_decimal) / 100
            data.payment_method = "card"
            data.payment_id = url_pay.id
            data.save()

        except stripe.error.StripeError as e:
            print(f"Error: {e}")
            return None


class PaymentStatus(generics.RetrieveAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]

    def get(self, request, pk):
        try:
            setting = get_object_or_404(Payments, id=pk)
            payment_id = str(setting.payment_id)
            stripe.api_key = settings.STRIPE_SECRET_KEY
            data_pay = stripe.checkout.Session.retrieve(payment_id)
            payment_status = data_pay.payment_status
            if payment_status == 'paid':
                setting.payment_status = True
                setting.save()
                return Response({'message': 'Курс оплачен'})
            else:
                return Response({'message': 'Курс неоплачен'})

        except stripe.error.StripeError as e:
            print(f'Error: {e}')
            return None


class PaymentsRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class SubscriptionCreateAPIView(generics.CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def perform_create(self, serializer):
        new_subscription = serializer.save(user=self.request.user)
        new_subscription.user = self.request.user
        new_subscription.is_subscribed = True
        new_subscription.save()


class SubscriptionDeleteAPIView(generics.DestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
