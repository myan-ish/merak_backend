from django.urls import path, include
from django.contrib.auth import views as auth_views

from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.routers import SimpleRouter

from user import views
from user import apis


router = SimpleRouter()
router.register("customer", views.CustomerViewSet)
router.register("", views.UserViewSet)

auth_urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", apis.RegistrationView.as_view(), name="registration"),
]

api_urlpatterns = [
    path("auth/", include(auth_urlpatterns)),
    path(
        "register_organization/",
        apis.OrganizationRegistrationView.as_view(),
        name="organization_registration",
    ),
    path("set_organization/", apis.set_user_organization, name="set_organization"),
]

urlpatterns = [
    path("", include(api_urlpatterns)),
    path("", include(router.urls)),
    path(
        "password_reset", apis.PasswordResetRequestView.as_view(), name="password_reset"
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        apis.password_reset_confirm,
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path(
        "activate/<str:token>/",
        apis.ActivateAccountView.as_view(),
        name="activate_account",
    ),
]
