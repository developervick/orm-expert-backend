from django.urls import path
from users.views import *

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('signup/veryfy-otp/', veryfy_otp, name='veryfy-otp'),
]