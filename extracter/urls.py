from django.urls import path

from extracter.views import Extracter

itsm = Extracter.as_view({"get": "itsm"})

urlpatterns = [
    path(r"api/v1/itsm/", itsm, name="itsm")
]
