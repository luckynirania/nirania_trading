# Generated by Django 4.2.5 on 2023-09-07 18:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("univest", "0011_order_exchange_order_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="ideastatus",
            name="order",
        ),
        migrations.AddField(
            model_name="order",
            name="idea_status",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="univest.ideastatus",
                verbose_name="Idea Status ID",
            ),
        ),
    ]
