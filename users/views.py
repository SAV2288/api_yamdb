from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import EmailSerializer, TokenGainSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import User, Confirmation_code
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from .managers import account_activation_token, get_tokens_for_user
from .permissions import AdminPermission
import datetime
from django.core.mail import send_mail
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework import generics


# Create your views here.

class EmailTokenView(APIView):
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            if User.objects.filter(email=email).exists():
                return Response({"Email адрес занят"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user = User.objects.create(email=email)
                code = account_activation_token.make_token(user)
                Confirmation_code.objects.create(user=user, code=code)
                send_mail(
                    'Подтверждение аккаунта',
                    'Ваш ключ активации {}'.format(code),
                    'yamb@mail.com',
                    [email],
                    fail_silently=True,
                )
            # return Response({"email : {}".format(email)})
            return Response({code})  # ТЕСТ ОТКЛЮЧИТЬ!!
            # return Response({"{Письмо с кодом активации отправлено на почту}"})
        raise ValidationError()


class JWTgetView(APIView):
    def post(self, request):
        serializer = TokenGainSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')

            try:
                user = User.objects.get(email=email)
            except:
                raise ValidationError('Юзер не найден')
            code = serializer.data.get('confirmation_code')
            if Confirmation_code.objects.filter(user=user, code=code).exists():
                user.is_active = True
                user.save()
                return Response(get_tokens_for_user(user))
            else:
                raise ValidationError("Не правельные данные")
        raise ValidationError()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AdminPermission,)
    pagination_class = PageNumberPagination


# #
class UserMeView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        user = request.user
        serializer = UserSerializer(instance=user,
                                    data=request.data,
                                    partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        raise ValidationError()


class UserView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminPermission,)
    lookup_field = 'username'
    #
    # def perform_update(self, serializer):
    #
    #     serializer.save()
