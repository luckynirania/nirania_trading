# Generated by Django 4.2.5 on 2023-09-11 03:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("angel_broking", "0002_alter_symboltokenmappingsheet_strike"),
    ]

    operations = [
        migrations.AlterField(
            model_name="symboltokenmappingsheet",
            name="tick_size",
            field=models.CharField(max_length=50),
        ),
    ]