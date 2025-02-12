import random
import string
import uuid

from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from .models import Session, CinemaUser
from datetime import datetime
from .serializers import SessionSerializer, TicketSerializer, UserSerializer
from random import randint


# Create your views here.


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_sessions(request: Request) -> Response:
    # получаем текущее время
    now = datetime.now()
    # получаем все сеансы, которые пройдут в будущем
    sessions = Session.objects.filter()
    # сериализуем и возвращаем в ответе
    serializer = SessionSerializer(sessions, many=True)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def buy_ticket(request: Request) -> Response:
    # парсим переданное бади, получая айди сеанса, айди юзера и место
    ticketJson = {
        "user": request.user.id,
        "sessionId": request.data.get('sessionId'),
        "seat": request.data.get('seat')
    }
    # создаем новый билет. Если айди сеанса или юзер не переданы, сервер вернет ошибку
    serializer = TicketSerializer(data=ticketJson)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
    return Response()


# генерит случайный пароль из букв+цифр+знаков длиной 12 символов
def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))


@api_view(['GET'])
@permission_classes([AllowAny])
def anon_auth(request: Request) -> Response:
    # генерим уид, чтобы избежать потенциальных совпадений
    user_uuid = str(uuid.uuid4())
    # юзернейм ставляем чисто уидом
    username = user_uuid
    # просто нейм, чтобы отобразить юзеру делаем более вменяемый
    first_name = f"Watcher{user_uuid[:8]}"
    # генерим случайный 12 символьный пароль
    password = generate_random_password()
    # создаем юзера
    user, created = CinemaUser.objects.get_or_create(username=username, defaults={
        'first_name': first_name
    })
    # устанавливаем хешированный пароль
    user.set_password(password)
    user.save()
    # возвращаем юзернейм и пароль в респонсе
    return Response({
        'username': username,
        'password': password
    })
