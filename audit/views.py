from rest_framework.viewsets import ModelViewSet
from audit.models import EntryItem, Ledger
from rest_framework.views import APIView
from audit.serializer import LedgerSerializer
from django.views.generic.base import View
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response

from user.models import Customer

# class ExpenseViewSet(ModelViewSet):
#     serializer_class = ExpenseSerializer
#     queryset = Expense.objects.all()

#     def get_queryset(self):
#         print(self.queryset.filter(organization=self.request.user.organization))
#         return self.queryset.filter(organization=self.request.user.organization)


# class ExpenseCategoryViewSet(ModelViewSet):
#     serializer_class = ExpenseCategorySerializer
#     queryset = ExpenseCategory.objects.all()

#     def get_queryset(self):
#         return self.queryset.filter(organization=self.request.user.organization)

class AuditView(View):
    template_name = "audit.html"
    
    def get(self, request):
        context = {
        "ledger": Ledger.objects.all(),
        }
        return render(request, self.template_name, context=context)

class LedgerViewSet(ModelViewSet):
    serializer_class = LedgerSerializer
    queryset = Ledger.objects.all()

    def get_queryset(self):
        return self.queryset.filter(organization=self.request.user.organization)

class Transaction(APIView):
    # TODO: Add permissions
    #       Add date to search ledger by certain fiscal year as there might be multiple ledgers for same customer
    def post(self, request):
        data = request.data
        related_user_id = data.get("related_user_id")
        related_user = get_object_or_404(Customer, id=related_user_id)
        ledger = get_object_or_404(Ledger, related_user=related_user)
        is_credit = ledger.is_credit(data.get("type"))
        items = [EntryItem.objects.create(
                product=item.get("product"),
                quantity=item.get("quantity"),
                price=item.get("price"),
            ).id for item in data.get("items")]
            
        ledger.make_transaction(data["amount"], items,is_credit, data.get("type"), data.get('vatable_discount'), data.get('non_vatable_discount'))
        return Response({"message": "Transaction made successfully"})
        