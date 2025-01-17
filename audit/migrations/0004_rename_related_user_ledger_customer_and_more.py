# Generated by Django 4.1.2 on 2022-10-30 04:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0002_product_vatable"),
        ("audit", "0003_ledger_organization"),
    ]

    operations = [
        migrations.RenameField(
            model_name="ledger",
            old_name="related_user",
            new_name="customer",
        ),
        migrations.RemoveField(
            model_name="entry",
            name="amount",
        ),
        migrations.AddField(
            model_name="entry",
            name="non_vatable_amount",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name="entry",
            name="non_vatable_discount",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name="entry",
            name="sub_total",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name="entry",
            name="total",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name="entry",
            name="vatable_amount",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name="entry",
            name="vatable_discount",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.CreateModel(
            name="EntryItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.IntegerField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "product",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inventory.product",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="entry",
            name="items",
            field=models.ManyToManyField(blank=True, to="audit.entryitem"),
        ),
    ]
