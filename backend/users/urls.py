from django.urls import path
from .views import SignUpView, SignInView, ProtectedRouteView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("signin/", SignInView.as_view(), name="signin"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("protected-route/", ProtectedRouteView.as_view(), name="protected_route"),
]
