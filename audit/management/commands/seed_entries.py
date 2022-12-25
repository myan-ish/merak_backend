from django.core.management.base import BaseCommand
from audit.models import Ledger, Entry, EntryItem, EntryTypeEnum
from inventory.models import Product
from user.models import Customer, Organization, User
import random
from django.core.exceptions import ValidationError


class Command(BaseCommand):
    help = "Seed entries for a year"

    def handle(self, *args, **options):
        organization = Organization.objects.create(
            name="test", owner=User.objects.get(email="admin@admin.com")
        )
        related_user = Customer.objects.create(name="test")
        product_list = [
            Product(
                name="test",
                price=random.randint(100, 10000),
                quantity=random.randint(100, 1000),
                organization=organization,
            )
            for i in range(10)
        ]
        Product.objects.bulk_create(product_list)

        entry_items = [
            EntryItem(
                product=Product.objects.get(id=random.randint(1, 10)),
                quantity=random.randint(100, 10000),
                price=random.randint(100, 1000),
            )
            for i in range(100)
        ]
        entry_items_created = EntryItem.objects.bulk_create(entry_items)

        for i in range(1, 12):
            for j in range(1, 31):
                try:
                    entry = Entry.objects.create(
                        is_credit=random.choice([True, False]),
                        type=random.choice(EntryTypeEnum.choices)[0],
                        date=f"2022-{i}-{j}",
                        closing_balance=random.randint(100, 1000),
                        vatable_amount=random.randint(100, 1000),
                        non_vatable_amount=random.randint(100, 1000),
                        vatable_discount=random.randint(100, 1000),
                        non_vatable_discount=random.randint(100, 1000),
                        total=random.randint(100, 1000),
                    )
                    entry.items.set(
                        entry_items_created[
                            random.randint(1, 50) : random.randint(51, 100)
                        ]
                    )
                    entry.save()
                except ValidationError:
                    pass

        self.stdout.write(
            self.style.SUCCESS("Successfully seeded test entries for a year")
        )
