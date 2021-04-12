from django.urls import path
from .views import catalogview

urlpatterns = [
    path("translations", catalogview, name="gettext_utils_catalog"),
]
