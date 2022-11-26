from rest_framework.viewsets import ModelViewSet
from audit.filters import LedgerFilter
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
    filter_class = LedgerFilter

    def get_queryset(self):
        return self.queryset.filter(organization=self.request.user.organization)
