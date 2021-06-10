from django.urls import path
from .views import CatalogView

urlpatterns = [
    path('translations', CatalogView.as_view(), name="gettext_utils_catalog")
]
