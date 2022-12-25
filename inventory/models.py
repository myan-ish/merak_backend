import uuid
from django.db import models

from user.models import Organization, User


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="product_images", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    opening_stock = models.IntegerField(default=0)
    current_stock = models.IntegerField(default=0)
    purchased_stock = models.IntegerField(default=0)
    sold_stock = models.IntegerField(default=0)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True
    )
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
        """
        The price in which the previous stock was bought at might be different from the current price. Here we are updating the price to the current price at which if the stock is sold, the profit will be made.
        It will also update the quantity of the stock.

        @param price: The price at which the stock is bought at.
        @param quantity: The quantity of the stock.
        """
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
