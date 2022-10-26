from rest_framework import serializers

from audit.models import Ledger

# from audit.models import Expense, ExpenseCategory
# from inventory.serializers.user import UserOutSerializer
# from user.models import User


# class ExpenseSerializer(serializers.ModelSerializer):
#     requested_user = UserOutSerializer(read_only=True, source="requested_by")
#     requested_by = serializers.PrimaryKeyRelatedField(
#         write_only=True, queryset=User.objects.all()
#     )

#     class Meta:
#         model = Expense
#         fields = "__all__"


# class ExpenseCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ExpenseCategory
#         fields = "__all__"

class LedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ledger
        fields = "__all__"