from django.urls import path
from django.urls import include
from .api import RegisterAPI
from knox import views as know_views
from .api import UserAPI
from .api import LoginAPI


urlpatterns = [
    path('api/auth', include('knox.urls')),
    path('api/auth/register', RegisterAPI.as_view()),
    path('api/auth/logout', know_views.LogoutView.as_view(), name='knox_logout'),
    path('api/auth/login', LoginAPI.as_view()),
    path('api/auth/user', UserAPI.as_view())
]

