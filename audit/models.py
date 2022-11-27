from decimal import Decimal
import uuid
from django.db import models, transaction

from user.models import Customer, Organization


class EntryItem(models.Model):
    product = models.ForeignKey(
        "inventory.Product", on_delete=models.CASCADE, null=True, blank=True
    )
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.product} - {self.quantity}"


class EntryTypeEnum(models.TextChoices):
    SALES_INVOICE = "SI", "Sales Invoice"  # Debit
    SALES_RETURN = "SR", "Sales Return"  # Credit
    PURCHASE_INVOICE = "PI", "Purchase Invoice"  # Credit
    PURCHASE_RETURN = "PR", "Purchase Return"  # Debit
    RECEIPT_VOUCHER = "RV", "Receipt Voucher"  # Credit
    PAYMENT_VOUCHER = "PV", "Payment Voucher"  # Debit
    JOURNAL_VOUCHER = "JV", "Journal Voucher"  # Debit/Credit


class Entry(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    date = models.DateField(auto_now=True)
    is_credit = models.BooleanField(default=False)
    closing_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    type = models.CharField(max_length=2, choices=EntryTypeEnum.choices)

    vatable_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    non_vatable_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    vatable_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    non_vatable_discount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    items = models.ManyToManyField(EntryItem, blank=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self) -> str:
        return f"{self.type} - {self.date} - {self.total}"

    def get_vatable_amount(self):
        vatable_amount = 0
        for item in self.items.all():
            if item.product.vatable:
                vatable_amount += item.price * item.quantity
        return Decimal(vatable_amount)

    def get_non_vatable_amount(self):
        non_vatable_amount = 0
        for item in self.items.all():
            if not item.product.vatable:
                non_vatable_amount += item.price * item.quantity
        return Decimal(non_vatable_amount)

    def get_sub_total(self):
        return Decimal(self.vatable_amount + self.non_vatable_amount)

    def get_total(self):
        """
        Returns the total amount of the entry after applying discounts and taxes.
        """
        sub_total = self.get_sub_total()
        if self.vatable_amount > 0:
            sub_total = (
                sub_total + (sub_total * Decimal(0.13)) - self.vatable_discount
            )  # Adding tax
        if self.non_vatable_amount > 0:
            sub_total = sub_total - self.non_vatable_discount
        return round(Decimal(sub_total), 2)


class LedgerTypeEnum(models.TextChoices):
    CAPITAL = "CAPITAL", "Capital"  # Credit
    FIXED_ASSET = "FIXED_ASSET", "Fixed Asset"  # Debit
    CURRENT_ASSSET = "CURRENT_ASSSET", "Current Asset"  # Debit
    LOAN_AND_ADVANCE = "LOAN_AND_ADVANCE", "Loan and Advance"  # Credit
    CASH_AND_BANK = "CASH_AND_BANK", "Cash and Bank"  # Credit
    INCOME = "INCOME", "Income"  # Debit
    LIABILITY = "LIABILITY", "Liability"  # Credit
    EXPENSE = "EXPENSE", "Expense"  # Debit
    CUSTOMER = "CUSTOMER", "Customer"  # Debit
    VENDOR = "VENDOR", "Vendor"  # Credit
    CUSTOMER_AND_VENDOR = "CUSTOMER_AND_VENDOR", "Customer and Vendor"  # Debit/Credit


class Ledger(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    type = models.CharField(
        max_length=255, choices=LedgerTypeEnum.choices, default=LedgerTypeEnum.CUSTOMER
    )
    date = models.DateField(auto_now=True)

    opening_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    closing_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        related_name="ledgers",
        null=True,
        blank=True,
    )

    entries = models.ManyToManyField(Entry, blank=True)

    credit = models.DecimalField(decimal_places=2, default=0, max_digits=15)
    debit = models.DecimalField(decimal_places=2, default=0, max_digits=15)

    def __str__(self):
        return self.name

    def is_credit(self, type):
        """
        Checks the type of entry and returns True if it is a credit entry.

        @param type: The type of entry
        """
        if type in [
            EntryTypeEnum.SALES_INVOICE,
            EntryTypeEnum.PURCHASE_RETURN,
            EntryTypeEnum.RECEIPT_VOUCHER,
            EntryTypeEnum.JOURNAL_VOUCHER,
        ]:
            return False
        return True

    @transaction.atomic
    def make_transaction(self, items, type, vatable_discount, non_vatable_discount):
        """
        This method is used to make a transaction in the ledger. It will create a new entry and add it to the ledger. It will also update the closing balance of the ledger.
        @param items: List of item's ids in the transaction
        @param is_credit: Boolean to indicate if the transaction is a credit or debit
        @param type: Type of transaction
        @param vatable_discount: Discount for vatable items
        @param non_vatable_discount: Discount for non vatable items
        """
        # TODO: Need to test this logic and function asap
        is_credit = self.is_credit(type)
        entry = Entry(
            is_credit,
            type=type,
            vatable_discount=vatable_discount,
            non_vatable_discount=non_vatable_discount,
        )

        entry.save()
        entry.items.set(items)

        entry.vatable_amount = entry.get_vatable_amount()
        entry.non_vatable_amount = entry.get_non_vatable_amount()
        entry.sub_total = entry.get_sub_total()
        entry.total = entry.get_total()

        self.closing_balance = (
            self.closing_balance + entry.total
            if not is_credit
            else self.closing_balance - entry.total
        )

        entry.closing_balance = self.closing_balance
        entry.save()
        entry.items.set(items)

        self.entries.add(entry)
        self.save()

    def save(self, *args, **kwargs):
        self.name = self.customer.name

        return super().save(*args, **kwargs)
