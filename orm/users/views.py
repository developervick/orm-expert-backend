from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from root.custom_jwt import get_tokens_for_user
from users.models import User
from django.core.mail import send_mail

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    print("signup")
    email = request.data.get('email')
    username = request.data.get('username')
    password = request.data.get('password')


    return Response({'status': 'success'})


@api_view(['POST'])
def login(request):
    return Response(get_tokens_for_user(request.user))

@api_view(['POST'])
def logout(request):
    return Response(get_tokens_for_user(request.user))


@api_view(['GET'])
@permission_classes([])
def sendmail(request):
    try:
        print("sending mail")
        send_mail(
            'Subject here',
            'Here is the message.',
            '6bZGt@example.com',
            ['6bZGt@example.com'],
            fail_silently=False,)
        print("mail sent")
        return Response({'status': 'success'})
    except Exception as e:
        print(e)
        return Response({'status': 'failed'})