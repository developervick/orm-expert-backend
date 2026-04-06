from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from root.custom_jwt import get_tokens_for_user
from users.models import User, OTP
import bcrypt
from users.utils import generate_random_otp, send_otp_on_mail
from django.db import transaction


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        name = request.data.get('name')

        if not email or not password or not confirm_password or not name:
            return Response({'status': 'all fields are required'}, status=400)

        if password != confirm_password:
            return Response({'status': 'passwords do not match'}, status=400)

        if User.objects.filter(email=email).exists():
            return Response({'status': 'email already exists'}, status=400)
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(10)).decode('utf-8')

        user = User.objects.create(email=email, first_name=name, password=hashed_password, role=User.Roles.USER, is_active=False)
        
        otp = generate_random_otp(4)
        otp_object = OTP.objects.create(email=email, otp=otp, is_expired=False, user=user)

        send_otp_on_mail(email, otp)
    
        return Response({"message": "otp sent to your email", "data": {"uuid": otp_object.uuid}, "error": None}, status=200)
    
    except Exception as e:
        print(e)
        return Response({'status': 'something went wrong'}, status=400)


@api_view(['POST'])
@permission_classes([AllowAny])
@transaction.atomic
def veryfy_otp(request):
    try:
        uuid = request.data.get('uuid')
        otp = request.data.get('otp')

        if not uuid or not otp:
            return Response({'status': 'all fields are required'}, status=400)

        otp_object = OTP.objects.select_related('user').filter(uuid=uuid).first()

        if not otp_object:
            return Response({'status': 'invalid uuid'}, status=400)

        if otp_object.is_expired:
            return Response({'status': 'otp is expired'}, status=400)

        if str(otp_object.otp) != str(otp):
            return Response({'status': 'invalid otp'}, status=400)

        otp_object.is_expired = True
        otp_object.user.is_active = True
        otp_object.user.save()
        otp_object.save()

        return Response({"message": "otp verified successfully", "data": get_tokens_for_user(otp_object.user), "error": None}, status=200)
    except Exception as e:
        print(e)
        return Response({'status': 'something went wrong'}, status=400)



@api_view(['POST'])
def login(request):
    return Response(get_tokens_for_user(request.user))

@api_view(['POST'])
def logout(request):
    return Response(get_tokens_for_user(request.user))

