import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from safedelete.models import SafeDeleteModel

from user.managers import CustomAccountManager


def get_upload_path_for_avatar(instance, filename):
    return f"avatars/users/{instance.id}/{filename}"

class GenderChoices(models.TextChoices):
    MALE = "MALE", _("Male")
    FEMALE = "FEMALE", _("Female")
    OTHER = "OTHER", _("Other")
    UNKNOWN = "UNKNOWN", _("Unknown")

class User(AbstractBaseUser, SafeDeleteModel, PermissionsMixin):
    email = models.EmailField(_("Email Address"), unique=True)
    first_name = models.CharField(max_length=64, null=True, blank=True)
    last_name = models.CharField(max_length=64, null=True, blank=True)
    avatar = models.ImageField(
        upload_to=get_upload_path_for_avatar, null=True, blank=True
    )
    gender = models.CharField(
        max_length=7, choices=GenderChoices.choices, null=True
    )
    birth_date = models.DateField(null=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.JSONField(null=True, blank=True)
    whatsapp = models.CharField(max_length=15, null=True, blank=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    class UserStatusChoice(models.TextChoices):
        PENDING = _("Pending")
        ACTIVE = _("Active")
        INACTIVE = _("Inactive")
        REMOVED = _("Removed")

    status = models.CharField(
        max_length=8,
        choices=UserStatusChoice.choices,
        default=UserStatusChoice.INACTIVE,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomAccountManager()

    def __str__(self):
        return self.email

    def delete(self, *args, **kwargs):
        self.status = User.UserStatusChoice.REMOVED
        super().delete(*args, **kwargs)

    def undelete(self, *args, **kwargs):
        self.status = User.UserStatusChoice.ACTIVE
        super().undelete(*args, **kwargs)

class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(null=True, blank=True, max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

class Organization(SafeDeleteModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="organizations"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uuid = models.CharField(max_length=6, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, keep_deleted=False, **kwargs):
        if not self.uuid:
            self.uuid = str(uuid.uuid4())[:6]
            while (
                Organization.objects.filter(uuid=self.uuid).exists()
            ):
                self.uuid = str(uuid.uuid4())[:6]
        return super().save(keep_deleted, **kwargs)
