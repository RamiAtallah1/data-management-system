from django.urls import include, path
from .views import index


urlpatterns = [
    path("", index, name="index"),
    path("api/schemas/", include("schema_manager.urls")),
    path("api/users/", include("users.urls")),
]
