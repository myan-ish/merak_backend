# Generated by Django 4.1.2 on 2022-10-30 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("audit", "0004_rename_related_user_ledger_customer_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ledger",
            name="closing_balance",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
        ),
        migrations.AlterField(
            model_name="ledger",
            name="opening_balance",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
        ),
    ]
