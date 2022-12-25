from rest_framework import serializers

from inventory.models import Category, Product
from user.models import Organization


class ProductOutSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(allow_blank=True, allow_null=True)
    image_url = serializers.CharField(allow_blank=True, allow_null=True)
    category = serializers.SerializerMethodField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    opening_stock = serializers.IntegerField()
    current_stock = serializers.IntegerField()
    purchased_stock = serializers.IntegerField()
    sold_stock = serializers.IntegerField()
    quantity = serializers.IntegerField()
    uuid = serializers.CharField(max_length=255, allow_blank=True, allow_null=True)
    vatable = serializers.BooleanField(default=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def get_category(self, obj):
        return obj.category.name


def StringOnlyValidator(value):
    if any(char.isdigit() for char in value):
        raise serializers.ValidationError("Must not contain number.")


class ProductInSerializer(serializers.ModelSerializer):
    category = serializers.CharField(validators=[StringOnlyValidator])

    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "image",
            "category",
            "price",
            "quantity",
            "vatable",
        ]

    def create(self, validated_data):
        validated_data["category"] = Category.objects.get_or_create(
            name=validated_data["category"],
            organization=self.context["request"].user.organization,
        )[0]
        validated_data["organization"] = self.context["request"].user.organization
        return super().create(validated_data)
