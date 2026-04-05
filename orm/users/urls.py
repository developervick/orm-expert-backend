from django.urls import path
from users.views import *

urlpatterns = [
    path('signup/', signup),
    path('login/', login),
    path('logout/', logout),
    path('sendmail/', sendmail),
]