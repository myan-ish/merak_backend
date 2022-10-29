# Generated by Django 4.1.2 on 2022-10-26 06:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0002_organization"),
        ("audit", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="ledger",
            name="organization",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="ledgers",
                to="user.organization",
            ),
        ),
    ]