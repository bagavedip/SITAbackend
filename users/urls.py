from django.urls import path
from rest_framework import routers

from users.views import UserViewSet

simple_router = routers.SimpleRouter()
login = UserViewSet.as_view({"post": "login"})

urlpatterns = simple_router.urls
urlpatterns = urlpatterns + [
    path(r"api/v1/login/", login, name="login")
]
