# Generated by Django 4.2.5 on 2023-09-11 02:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("univest", "0013_alter_order_amount"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="order_sub_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("GTT", "GTT"),
                    ("MARKET", "Market"),
                    ("LIMIT", "Limit"),
                    ("STOP_LOSS", "Stop Loss"),
                ],
                max_length=20,
                verbose_name="Order Sub Type",
            ),
        ),
        migrations.AlterField(
            model_name="ideastatus",
            name="status",
            field=models.CharField(
                choices=[
                    ("NEW", "New"),
                    ("BUY_ORDER_PLACED", "Buy Order Placed"),
                    ("BUY_ORDER_CANCELLED", "Buy Order Cancelled"),
                    ("BOUGHT", "Bought"),
                    ("SELL_ORDER_PLACED", "Sell Order Placed"),
                    ("SELL_ORDER_CANCELLED", "Sell Order Cancelled"),
                    ("SOLD", "Sold and Closed"),
                    ("EXPIRED", "Idea was already Closed"),
                ],
                default="NEW",
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="order_type",
            field=models.CharField(
                blank=True,
                choices=[("SELL", "Sell"), ("BUY", "Buy")],
                max_length=20,
                verbose_name="Order Type",
            ),
        ),
    ]
