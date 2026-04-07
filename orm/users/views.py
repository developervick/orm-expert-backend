from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from root.custom_jwt import get_tokens_for_user
from users.models import User, OTP
import bcrypt
from users.utils import generate_random_otp, send_otp_on_mail
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        name = request.data.get('name')

        if not email or not password or not confirm_password or not name:
            return Response({'status': 'all fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        if password != confirm_password:
            return Response({'status': 'passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'status': 'email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(10)).decode('utf-8')

        user = User.objects.create(email=email, first_name=name, password=hashed_password, role=User.Roles.USER, is_active=False)
        
        otp = generate_random_otp(4)
        otp_object = OTP.objects.create(email=email, otp=otp, is_expired=False, user=user)

        send_otp_on_mail(email, otp)
    
        return Response({"message": "otp sent to your email", "data": {"uuid": otp_object.uuid}, "error": None}, status=status.HTTP_200_OK)
    
    except Exception as e:
        print(e)
        return Response({'status': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
@transaction.atomic
def verify_otp(request):
    try:
        uuid = request.data.get('uuid')
        otp = request.data.get('otp')

        if not uuid or not otp:
            return Response({'error': 'all fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        otp_object = OTP.objects.select_related('user').filter(uuid=uuid).first()

        if not otp_object:
            return Response({'error': 'invalid uuid'}, status=status.HTTP_400_BAD_REQUEST)

        if otp_object.is_expired:
            return Response({'error': 'otp is expired'}, status=status.HTTP_400_BAD_REQUEST)

        if str(otp_object.otp) != str(otp):
            return Response({'error': 'invalid otp'}, status=status.HTTP_400_BAD_REQUEST)

        otp_object.is_expired = True
        otp_object.user.is_active = True
        otp_object.user.save()
        otp_object.save()

        return Response({"message": "otp verified successfully", "data": {"tokens": get_tokens_for_user(otp_object.user), "userId": otp_object.user.id}, "error": None}, status=200)
    except Exception as e:
        print(e)
        return Response({'status': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'all fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()

        if not user:
            return Response({'error': 'user does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        if not user.is_active:
            return Response({'error': 'user is not active'}, status=status.HTTP_400_BAD_REQUEST)

        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return Response({'error': 'invalid credentials'}, status=400)

        return Response({"message": "login successful", "data": {"tokens": get_tokens_for_user(user), "userId": user.id, "role": [user.role], "email": user.email}, "error": None}, status=status.HTTP_200_OK)
    
    except Exception as e:
        print(e)
        return Response({'error': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def logout(request):
    try:

        
        if not request.user.is_authenticated:
            return Response({'error': 'user is not authenticated'}, status=status.HTTP_400_BAD_REQUEST)
        
        refres_token = request.data.get('refresh')

        if not refres_token:
            return Response({'error': 'refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        token = RefreshToken(refres_token)
        token.blacklist()
        
        return Response({"message": "logout successful", "data": None, "error": None}, status=status.HTTP_200_OK)
    
    except Exception as e:
        print(e)
        return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)

