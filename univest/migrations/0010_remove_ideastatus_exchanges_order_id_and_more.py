# Generated by Django 4.2.5 on 2023-09-07 17:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("univest", "0009_alter_ideastatus_status"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="ideastatus",
            name="exchanges_order_id",
        ),
        migrations.AddField(
            model_name="ideastatus",
            name="order",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="univest.order",
                verbose_name="Order ID",
            ),
        ),
    ]
