from django_filters import rest_framework as filters
from django.db.models import Q

from audit.models import Ledger


class LedgerFilter(filters.FilterSet):
    class Meta:
        model = Ledger
        fields = {
            "date": ["exact"],
        }
