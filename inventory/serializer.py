from rest_framework import serializers

from inventory.models import Product
from user.models import Organization


class ProductOutSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(allow_blank=True, allow_null=True)
    image_url = serializers.CharField(allow_blank=True, allow_null=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField()
    uuid = serializers.CharField(max_length=255, allow_blank=True, allow_null=True)
    vatable = serializers.BooleanField(default=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class ProductInSerializer(serializers.Serializer):
    class Meta:
        model = Product
        fields = "__all__"
