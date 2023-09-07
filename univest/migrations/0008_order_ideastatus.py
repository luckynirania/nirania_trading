# Generated by Django 4.2.5 on 2023-09-07 17:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("univest", "0007_delete_historicalidea"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
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
                (
                    "order_type",
                    models.CharField(
                        choices=[
                            ("SELL", "Sell"),
                            ("BUY", "Buy"),
                            ("GTT_SELL", "GTT Sell"),
                            ("GTT_BUY", "GTT Buy"),
                        ],
                        max_length=20,
                        verbose_name="Order Type",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PLACED", "Placed"),
                            ("CANCELLED", "Cancelled"),
                            ("EXECUTED", "Executed"),
                        ],
                        max_length=20,
                        verbose_name="Status",
                    ),
                ),
                ("price", models.FloatField(verbose_name="Price")),
                ("quantity", models.IntegerField(verbose_name="Quantity")),
                ("amount", models.FloatField(verbose_name="Amount")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created At"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated At"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="IdeaStatus",
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
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("NEW", "New"),
                            ("BUY_ORDER_PLACED", "Buy Order Placed"),
                            ("BOUGHT", "Bought"),
                            ("SELL_GTT_ORDER_PLACED", "Sell GTT Order Placed"),
                            ("SOLD", "Sold"),
                        ],
                        default="NEW",
                        max_length=50,
                    ),
                ),
                (
                    "exchanges_order_id",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "idea",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="univest.idea"
                    ),
                ),
            ],
        ),
    ]