# Generated by Django 4.2.5 on 2023-09-07 17:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("univest", "0008_order_ideastatus"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ideastatus",
            name="status",
            field=models.CharField(
                choices=[
                    ("NEW", "New"),
                    ("BUY_ORDER_PLACED", "Buy Order Placed"),
                    ("BOUGHT", "Bought"),
                    ("SELL_GTT_ORDER_PLACED", "Sell GTT Order Placed"),
                    ("SOLD", "Sold and Closed"),
                    ("EXPIRED", "Idea was already Closed"),
                ],
                default="NEW",
                max_length=50,
            ),
        ),
    ]