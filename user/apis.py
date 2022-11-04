import base64
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import SetPasswordForm
from django.conf import settings
from django.http import BadHeaderError
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.db import transaction
from django.db.models.query_utils import Q

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import Organization

from .serializers import (
    OrganizationRegistrationSerializer,
    RegistrationSerializer,
    ResendVerificationEmailSerializer,
    PasswordResetRequestSerializer,
)

User = get_user_model()


class RegistrationView(generics.CreateAPIView):
    model = User
    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            return Response(
                {"access_token": str(RefreshToken.for_user(user).access_token)},
                status=201,
            )


class ResendVerificationEmailView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = ResendVerificationEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class PasswordResetRequestView(APIView):
    http_method_names = ["post"]
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serialized_data = serializer.data
            associated_users = User.objects.filter(Q(email=serialized_data["email"]))
            if associated_users.exists():
                for user in associated_users:
                    # TODO: CHANGE TO JOD SCEDULE
                    subject = "Merak - Password Reset Required"
                    email_template_name = "password_reset_email.txt"
                    context = {
                        "email": user.email,
                        "domain": get_current_site(request),
                        "site_name": "Merak",
                        "uid": base64.urlsafe_b64encode(force_bytes(user.pk)).decode(),
                        "user": user,
                        "token": default_token_generator.make_token(user),
                        "protocol": "http",
                    }
                    email = render_to_string(email_template_name, context)
                    try:
                        send_mail(
                            subject,
                            email,
                            settings.EMAIL_HOST_USER,
                            [user.email],
                            fail_silently=False,
                        )
                        return Response(
                            {"message": "Email sent successfully."},
                            status=status.HTTP_200_OK,
                        )
                    except BadHeaderError:
                        return Response(
                            {"message": "Email sent successfully."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        )
                    except Exception as ex:
                        return Response(
                            {"message": "Email is not sent to the user"},
                            status=status.HTTP_412_PRECONDITION_FAILED,
                        )
            else:
                return Response(
                    {"message": "User doesn't exist"},
                    status=status.HTTP_412_PRECONDITION_FAILED,
                )
        else:
            return Response(
                serializer.errors, status=status.HTTP_428_PRECONDITION_REQUIRED
            )


def password_reset_confirm(request, uidb64, token):
    if request.method == "GET":
        if (uidb64) and (token):
            print(force_str(base64.urlsafe_b64decode(uidb64).decode()))
            user = User.objects.filter(
                id=force_str(base64.urlsafe_b64decode(uidb64).decode())
            ).first()
            form = SetPasswordForm(user=user)
            return render(
                request=request,
                template_name="password_reset_confirm.html",
                context={"set_password_form": form},
            )
    else:
        if request.POST.get("new_password1") == request.POST.get("new_password2"):
            user = User.objects.filter(
                id=force_str(base64.urlsafe_b64decode(uidb64).decode())
            ).first()
            user.set_password(request.POST.get("new_password1"))
            user.save()
        return redirect("password_reset_complete")


class OrganizationRegistrationView(generics.ListAPIView):
    serializer_class = OrganizationRegistrationSerializer

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            data = request.data
            data["owner"] = request.user.id
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()
            return Response(
                {
                    "data": serializer.data,
                    "message": "Organization created successfully.",
                },
                status=201,
            )


def set_user_organization(request):
    if request.method == "POST":
        user = request.user
        organization_uuid = request.POST.get("organization_uuid")
        if organization_uuid:
            try:
                organization = Organization.objects.get(uuid=organization_uuid)
            except Organization.DoesNotExist:
                return Response(
                    {"message": "Organization does not exist."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            user.organization = organization
            user.save()
            return Response(
                {"message": "Organization set successfully."},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "Organization uuid is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        return Response(
            {"message": "Invalid request method."},
            status=status.HTTP_400_BAD_REQUEST,
        )
