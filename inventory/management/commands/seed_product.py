import uuid
from django.core.management.base import BaseCommand
from inventory.models import Product
from user.models import Organization, User
import random


class Command(BaseCommand):
    help = "Seed 100000 products"

    def handle(self, *args, **options):
        Product.objects.all().delete()
        organization = Organization.objects.filter(
            owner=User.objects.get(email="admin@admin.com"), name="SX-GLV Inc."
        )[0]
        product_list = []
        for i in range(100000):
            product_list.append(
                Product(
                    name="test",
                    description="seeded_data",
                    price=random.randrange(100, 1000),
                    quantity=random.randrange(100, 1000),
                    organization=organization,
                    uuid=str(uuid.uuid4())[:8],
                )
            )
        Product.objects.bulk_create(product_list)
        self.stdout.write(self.style.SUCCESS("Successfully seeded 100000 products"))
