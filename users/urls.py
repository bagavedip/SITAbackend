from django.urls import path
from users.views import UserViewSet


login = UserViewSet.as_view({"post": "login"})


urlpatterns = [
    path(r"login/", login, name="login"),
]
