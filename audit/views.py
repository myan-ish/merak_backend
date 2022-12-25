from django.views.generic.base import View
from django.shortcuts import get_object_or_404, render

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.decorators import action


from audit.filters import LedgerFilter
from audit.models import Entry, EntryItem, Ledger
from audit.serializer import LedgerSerializer
from audit.service import (
    get_products_sold_for_within_a_month,
    get_projected_gross_profit_for_the_year,
    get_total_transaction_for_a_month,
)

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


class DashboardViewSet(ViewSet):
    @action(
        detail=False,
        methods=["get"],
        url_path="total_transaction_for_a_month/(?P<month>[0-9]+)",
    )
    def get_total_transaction_for_a_month(self, request, month):
        valid_entires = Entry.objects.filter(
            ledger__in=Ledger.objects.filter(organization=request.user.organization)
        )
        total = get_total_transaction_for_a_month(valid_entires, month)
        return Response({"total": total})

    @action(
        detail=False,
        methods=["get"],
        url_path="get_products_sold_for_within_a_month/(?P<month>[0-9]+)",
    )
    def get_products_sold_for_within_a_month(self, request, month):
        valid_entires = Entry.objects.filter(
            ledger__in=Ledger.objects.filter(organization=request.user.organization)
        )
        products = get_products_sold_for_within_a_month(valid_entires, month)
        return Response({"products": products})

    @action(detail=False, methods=["get"], url_path="get_projected_gross_profit")
    def get_projected_gross_profit(self, request):
        valid_entires = Entry.objects.filter(
            ledger__in=Ledger.objects.filter(organization=request.user.organization)
        )
        gross_profit = get_projected_gross_profit_for_the_year(valid_entires)
        return Response({"gross_profit": gross_profit})


def remove_entry():
    Entry.objects.all().delete()
    EntryItem.objects.all().delete()
