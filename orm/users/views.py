from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from root.custom_jwt import get_tokens_for_user

class user():
    id = 1
    name: "user"

@api_view(['GET'])
def home(req):
    return Response({"token": get_tokens_for_user(user())})