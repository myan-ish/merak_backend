from django.shortcuts import get_object_or_404
from audit.models import EntryItem, Ledger
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.views import APIView
from audit.serializer import TransactionSerializer
from inventory.models import Product

from user.models import Customer


class get_current_balance(APIView):
    """
    Returns the current audit balance
    """

    def get(self, request):
        current_balance = Ledger.objects.aggregate(Sum("closing_balance"))
        return Response({"current_balance": current_balance})


class Transaction(APIView):
    # TODO: Add permissions
    #       Add date to search ledger by certain fiscal year as there might be multiple ledgers for same customer
    serializer_class = TransactionSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        customer = data.get("customer")
        customer = get_object_or_404(Customer, pk=customer)
        ledger = get_object_or_404(Ledger, customer=customer)
        # is_credit = ledger.is_credit(data.get("type"))
        items = [
            EntryItem.objects.create(
                product=get_object_or_404(Product, pk=item.get("product")),
                quantity=item.get("quantity"),
                price=item.get("price"),
            )
            for item in data.get("items")
        ]

        ledger.make_transaction(
            items,
            # is_credit,
            data.get("type"),
            data.get("vatable_discount"),
            data.get("non_vatable_discount"),
        )
        return Response(
            {
                "message": "Transaction made successfully",
                "ledger": ledger.id,
                "closing_balance": ledger.closing_balance,
            },
        )
