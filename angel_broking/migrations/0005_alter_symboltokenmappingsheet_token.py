# Generated by Django 4.2.5 on 2023-09-11 03:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("angel_broking", "0004_alter_symboltokenmappingsheet_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="symboltokenmappingsheet",
            name="token",
            field=models.CharField(max_length=50),
        ),
    ]
