from django.urls import path, include
from rest_framework import routers
from inventory.views import ProductViewSet

router = routers.DefaultRouter()

# router.register("expense", ExpenseViewSet)
# router.register("expense_category", ExpenseCategoryViewSet)
router.register("product", ProductViewSet)


api_patterns = []

urlpatterns = [
    path("", include(router.urls)),
    path("", include(api_patterns)),
]
