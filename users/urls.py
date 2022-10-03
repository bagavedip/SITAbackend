from django.urls import path
from rest_framework import routers

from users.views.users import UserViewSet
from users.views.update_profile import UserUpdate
from users.views.update_password import PasswordUpdate

simple_router = routers.SimpleRouter()
login = UserViewSet.as_view({"post": "login"})
add_user = UserViewSet.as_view({"post": "add_user"})
update_user = UserUpdate.as_view({"post": "update_name"})
update_user_password = PasswordUpdate.as_view({"post": "update_password"})

urlpatterns = simple_router.urls
urlpatterns = urlpatterns + [
    path(r"api/v1/login/", login, name="login"),
    path(r"api/v1/add_user/", add_user, name="add_user"),
    path(r"api/v1/update_user/", update_user, name="update_user"),
    path(r"api/v1/update_password/", update_user_password, name="update_user_password")
]
