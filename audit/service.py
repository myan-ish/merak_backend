from datetime import datetime
from audit.models import EntryItem, Ledger, Entry

from django.db.models import Sum


def get_total_transaction_for_a_month(entries, month):
    total = entries.filter(date__month=month).aggregate(Sum("total"))
    return total


def get_products_sold_for_within_a_month(entries, month):
    products = (
        entries.filter(date__month=month)
        .values("items__product")
        .annotate(total_quantity=Sum("items__quantity"))
    )
    return products

    # def get_projected_gross_profit_for_the_year(entries):
    # Use the existing entries to project the gross profit for the year by using simple linear regression

    current_month = datetime.now().month

    # Get the total sales till the current month with month as key and total as value
    entry_till_now = [
        entries.filter(date__month=i).values("date__month").annotate(total=Sum("total"))
        for i in range(1, current_month)
    ]

    # Get the factor by which the sales are increasing by looking at the last 3 months, assuming linear growth
    factor = (
        entry_till_now[current_month - 2][0]["total"]
        - entry_till_now[current_month - 3][0]["total"]
    ) / entry_till_now[current_month - 3][0]["total"]

    # Get the total sales from this month till the end of the year by multiplying the factor
    projected_sales = [
        entry_till_now[current_month - 2][0]["total"] * (1 + factor) ** i
        for i in range(1, 13 - current_month + 1)
    ]

    # Create a new dictionay with month as key and total as value for the projected sales from entry_till_now and projected_sales
    entry_till_now = {
        i: entry_till_now[i][0]["total"] for i in range(0, current_month - 1)
    }

    projected_sales = {
        i: projected_sales[i - current_month + 1] for i in range(current_month - 1, 12)
    }

    # Merge the two dictionaries
    entry_till_now.update(projected_sales)
    return entry_till_now


def get_projected_gross_profit_for_the_year(entries):
    # Use the existing entries to project the gross profit for the year by using simple linear regression

    current_month = datetime.now().month

    # Get the total sales till the current month with month as key and total as value
    entry_till_now = [
        entries.filter(date__month=i).values("date__month").annotate(total=Sum("total"))
        for i in range(1, current_month)
    ]

    # Get the factor by which the sales are increasing by looking at the last 3 months, assuming linear growth
    try:
        income_of_a_month_ago = entry_till_now[current_month - 2][0]["total"]
    except IndexError:
        income_of_a_month_ago = 0

    try:
        income_of_two_months_ago = entry_till_now[current_month - 3][0]["total"]
    except IndexError:
        income_of_two_months_ago = 0

    try:
        factor = (
            income_of_a_month_ago - income_of_two_months_ago
        ) / income_of_two_months_ago
    except ZeroDivisionError:
        factor = 1

    print(factor)

    # Get the total sales from this month till the next 12 months by multiplying the factor
    projected_sales = [income_of_a_month_ago * (1 + factor) ** i for i in range(1, 13)]

    projected_sales_dict = {}
    for i in range(current_month + 1, 13 + current_month):
        if i > 12:
            i = i - 12
        projected_sales_dict[i] = projected_sales[i - current_month - 1]
    print(projected_sales_dict)
    return projected_sales_dict
