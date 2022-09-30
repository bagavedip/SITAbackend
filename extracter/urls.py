from django.urls import path

from extracter.views import Extracter

itsm = Extracter.as_view({"get": "itsm"})
soar = Extracter.as_view({"get": "soar"})

urlpatterns = [
    path(r"api/v1/itsm/", itsm, name="itsm"),
    path(r"api/v1/soar/", soar, name="soar")
]
