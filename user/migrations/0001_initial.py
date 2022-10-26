# Generated by Django 4.1.2 on 2022-10-26 05:51

from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("phone", models.CharField(blank=True, max_length=20, null=True)),
                ("address", models.CharField(blank=True, max_length=100, null=True)),
                ("latitude", models.FloatField(blank=True, null=True)),
                ("longitude", models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "deleted",
                    models.DateTimeField(db_index=True, editable=False, null=True),
                ),
                (
                    "deleted_by_cascade",
                    models.BooleanField(default=False, editable=False),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="Email Address"
                    ),
                ),
                ("first_name", models.CharField(blank=True, max_length=64, null=True)),
                ("last_name", models.CharField(blank=True, max_length=64, null=True)),
                (
                    "avatar",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=user.models.get_upload_path_for_avatar,
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[
                            ("MALE", "Male"),
                            ("FEMALE", "Female"),
                            ("OTHER", "Other"),
                            ("UNKNOWN", "Unknown"),
                        ],
                        max_length=7,
                        null=True,
                    ),
                ),
                ("birth_date", models.DateField(null=True)),
                ("phone", models.CharField(blank=True, max_length=20, null=True)),
                ("address", models.JSONField(blank=True, null=True)),
                ("whatsapp", models.CharField(blank=True, max_length=15, null=True)),
                ("is_admin", models.BooleanField(default=False)),
                ("is_staff", models.BooleanField(default=False)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Pending", "Pending"),
                            ("Active", "Active"),
                            ("Inactive", "Inactive"),
                            ("Removed", "Removed"),
                        ],
                        default="Inactive",
                        max_length=8,
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
