from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group
from django import forms

from .models import Customer, Organization, User
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ("email", "is_staff", "status")
    list_filter = ("email", "is_staff", "status")
    fieldsets = (
<<<<<<< Updated upstream
=======
<<<<<<< Updated upstream
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff',)}),
=======
>>>>>>> Stashed changes
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "status")}),
        (
            "Personal info",
<<<<<<< Updated upstream
            {"fields": ("first_name", "last_name", "phone", "organization")},
        ),
=======
            {"fields": ("first_name", "last_name", "phone", "organization", "avatar")},
        ),
>>>>>>> Stashed changes
>>>>>>> Stashed changes
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


class GroupAdminForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        User.objects.all(),
        widget=admin.widgets.FilteredSelectMultiple("Users", False),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            initial_users = self.instance.user_set.values_list("pk", flat=True)
            self.initial["users"] = initial_users

    def save(self, *args, **kwargs):
        kwargs["commit"] = True
        return super(GroupAdminForm, self).save(*args, **kwargs)

    def save_m2m(self):
        self.instance.user_set.clear()
        self.instance.user_set.add(*self.cleaned_data["users"])


class GroupAdmin(GroupAdmin):
    form = GroupAdminForm


admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Customer)
admin.site.register(Organization)
