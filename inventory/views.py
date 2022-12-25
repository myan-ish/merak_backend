from django.shortcuts import render
from inventory.models import Product
from inventory.serializer import ProductOutSerializer, ProductInSerializer

from rest_framework import viewsets


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductOutSerializer
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return ProductOutSerializer
        return ProductInSerializer

    def get_queryset(self):
        return self.queryset.filter(
            organization=self.request.user.organization
        ).order_by("-created_at")