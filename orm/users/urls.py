from django.urls import path
from users.views import *

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('signup/verify-otp/', verify_otp, name='verify-otp'),
    path('token/refresh/', RefreshTokenView.as_view()),
]