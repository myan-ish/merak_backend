import uuid
from django.db import models

from user.models import Organization, User


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="product_images", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    category = models.CharField(max_length=255, blank=True, null=True)
    uuid = models.CharField(max_length=255, blank=True, null=True, unique=True)

    vatable = models.BooleanField(default=True)

    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.uuid

    def add_stock(self, price, quantity):
        # since the price of stock might fluctuate, we need to update the price of the product according to the added stock against existing stock
        if self.quantity > 0:
            self.price = (self.price * self.quantity + price * quantity) / (
                self.quantity + quantity
            )
        else:
            self.price = price
        self.quantity += quantity
        self.save()

    def save(self, *args, **kwargs):
        # generate uuid
        if not self.uuid:
            self.uuid = str(uuid.uuid4())[:8]
            while Product.objects.filter(uuid=self.uuid).exists():
                self.uuid = str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)
