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
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.views import APIView

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
        tokens = get_tokens_for_user(otp_object.user)
        response =  Response({"message": "otp verified successfully", "data": {"tokens": tokens, "userId": otp_object.user.id}, "error": None}, status=200)
        response.set_cookie('refreshToken', tokens['refresh'], httponly=True, secure=True, samesite='None')
        response.set_cookie('accessToken', tokens['access'], httponly=True, secure=True, samesite='None')
        return response
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
        tokens = get_tokens_for_user(user)
        response =  Response({"message": "login successful", "data": {"tokens": tokens, "userId": user.id, "role": [user.role], "email": user.email}, "error": None}, status=status.HTTP_200_OK)
        response.set_cookie('refreshToken', tokens['refresh'], httponly=True, secure=True, samesite='None', max_age=7*24*60*60)
        return response
    
    except Exception as e:
        print(e)
        return Response({'error': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def logout(request):
    try:
        response = Response({
            'message': 'Logged out',
            'data': None,
            'error': None
        })

        # ✅ Clear the httpOnly cookie
        response.delete_cookie(
            key='refresh_token',
            samesite='Strict'
        )

        return response
            
    except Exception as e:
        print(e)
        return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)
    

class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Read refresh token from httpOnly cookie
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response({
                'message': 'No refresh token',
                'data': None,
                'error': 1
            }, status=401)

        try:
            refresh = RefreshToken(refresh_token)
            new_access_token = str(refresh.access_token)

            response = Response({
                'message': 'Token refreshed',
                'data': { 'access': new_access_token },  # ✅ new access token in body
                'error': 0
            })

            # ✅ Rotate — set new refresh token in cookie
            response.set_cookie(
                key='refresh_token',
                value=str(refresh),
                httponly=True,
                secure=True,
                samesite='Strict',
                max_age=7 * 24 * 60 * 60
            )

            return response

        except TokenError:
            return Response({
                'message': 'Invalid or expired refresh token',
                'data': None,
                'error': 1
            }, status=401)

