# Generated by Django 2.2.10 on 2020-03-05 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("payment", "0030_auto_20190916_1421")]

    operations = [
        migrations.AddField(
            model_name="paymenttransaction",
            name="source",
            field=models.CharField(
                choices=[
                    ("stripe", "Stripe"),
                    ("cash", "Kontant"),
                    ("shop", "Kiosk"),
                    ("transfer", "Overføring"),
                ],
                default="cash",
                max_length=64,
            ),
            preserve_default=False,
        )
    ]