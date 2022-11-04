from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.hashers import check_password
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from user.models import Organization

from .validators import validate_password
from .services.auth_handlers import create_verification_link

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField()

    @staticmethod
    def get_display_name(obj):
        return f"{obj.first_name} {obj.last_name}"

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "status",
            "avatar",
            "gender",
            "display_name",
            "birth_date",
            "phone",
            "address",
            "whatsapp",
            "is_superuser",
            "is_admin",
            "is_staff",
        )


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "old_password",
            "new_password",
        )

    def validate(self, data: dict) -> dict:
        old_password, new_password = data["old_password"], data["new_password"]

        if not check_password(old_password, self.instance.password):
            raise serializers.ValidationError(
                {"old_password": _("Password isn't correct")}
            )
        try:
            password_validation.validate_password(password=new_password)
        except password_validation.ValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})

        return data

    def update(self, instance: User, validated_data: dict) -> User:
        instance.set_password(validated_data["new_password"])
        instance.save(update_fields=("password",))
        return instance


class AuthSerializer(serializers.Serializer):
    access_token = serializers.CharField(
        max_length=4096, required=True, trim_whitespace=True
    )


class RegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=64)
    last_name = serializers.CharField(max_length=64)
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "password",
        )

    def create(self, validated_data: dict) -> dict:
        user = User.objects.create_user(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
            password=validated_data["password"],
            status=User.UserStatusChoice.PENDING,
        )
        return user


class ResendVerificationEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data: dict) -> dict:
        email = data["email"]
        try:
            user = User.objects.get(email=email, status=User.UserStatusChoice.PENDING)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"error": _("Email is not valid or user is not pending")}
            )

        verification_url, token = create_verification_link(user)
        # TODO: EMAIL VERIFICATION JOB SCEDULE
        return data


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)


class OrganizationRegistrationSerializer(serializers.ModelSerializer):
    owner = serializers.IntegerField(write_only=True)
    uuid = serializers.UUIDField(read_only=True)

    class Meta:
        model = Organization
        fields = (
            "name",
            "description",
            "owner",
            "uuid",
        )

    def create(self, validated_data: dict) -> dict:
        validated_data["owner"] = User.objects.get(id=validated_data["owner"])
        organization = Organization.objects.create(
            name=validated_data["name"],
            description=validated_data["description"],
            owner=validated_data["owner"],
        )
        print(organization.id, organization.uuid)
        return organization
