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

class TransactionEntryItemSerializer(serializers.Serializer):
    product = serializers.IntegerField()
    quantity = serializers.IntegerField()
    price = serializers.IntegerField()

class TransactionSerializer(serializers.Serializer):
    customer = serializers.IntegerField()
    type = serializers.CharField()
    items = serializers.ListField()
    vatable_discount = serializers.DecimalField(max_digits=10, decimal_places=2)
    non_vatable_discount = serializers.DecimalField(max_digits=10, decimal_places=2)