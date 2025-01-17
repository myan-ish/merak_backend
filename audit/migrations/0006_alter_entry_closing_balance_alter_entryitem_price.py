# Generated by Django 4.1.2 on 2022-10-30 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("audit", "0005_alter_ledger_closing_balance_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="entry",
            name="closing_balance",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
        ),
        migrations.AlterField(
            model_name="entryitem",
            name="price",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
