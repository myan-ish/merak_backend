from django.core.management.base import BaseCommand
from audit.models import Ledger
from user.models import Customer, Organization, User
import random


class Command(BaseCommand):
    help = "Seed 100000 ledgers"

    def handle(self, *args, **options):
        organization = Organization.objects.create(
            name="test", owner=User.objects.get(email="admin@admin.com")
        )
        related_user = Customer.objects.create(name="test")
        ledger_list = []
        for i in range(100000):
            ledger_list.append(
                Ledger(
                    name="test",
                    type="CAPITAL",
                    opening_balance=random.randint(100, 10000),
                    closing_balance=random.randint(100, 1000),
                    organization=organization,
                )
            )
        Ledger.objects.bulk_create(ledger_list)
        self.stdout.write(self.style.SUCCESS("Successfully seeded 100000 ledgers"))
