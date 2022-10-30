from django.contrib import admin

from audit.models import Entry, EntryItem, Ledger

class EntryAdmin(admin.ModelAdmin):
    list_display = ["total", "type", "date","credit"]
    list_filter = ["date"]

    def credit(self, obj):
        return obj.is_credit

    credit.boolean = True

class LedgerAdmin(admin.ModelAdmin):
    list_display = ["name", "type", "opening_balance", "closing_balance", "customer"]
    list_filter = ["type"]

admin.site.register(Entry, EntryAdmin)
admin.site.register(Ledger, LedgerAdmin)
admin.site.register(EntryItem)