from django.contrib import admin

from audit.models import Entry, Ledger

class EntryAdmin(admin.ModelAdmin):
    list_display = ["amount", "type", "date","credit"]
    list_filter = ["date"]

    def credit(self, obj):
        return obj.is_credit

    credit.boolean = True

class LedgerAdmin(admin.ModelAdmin):
    list_display = ["name", "type", "opening_balance", "closing_balance", "related_user"]
    list_filter = ["type"]

admin.site.register(Entry, EntryAdmin)
admin.site.register(Ledger, LedgerAdmin)