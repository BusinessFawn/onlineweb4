# Generated by Django 2.2.10 on 2020-02-22 13:36

import apps.authentication.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("authentication", "0044_auto_20200220_1537")]

    operations = [
        migrations.AddField(
            model_name="onlinegroup",
            name="admin_roles",
            field=models.ManyToManyField(
                default=apps.authentication.models.get_default_group_roles,
                help_text="Roller som kan administrere denne gruppen og undergrupper",
                related_name="admin_for_groups",
                to="authentication.GroupRole",
                verbose_name="Administrerende roller",
            ),
        ),
        migrations.AddField(
            model_name="onlinegroup",
            name="roles",
            field=models.ManyToManyField(
                default=apps.authentication.models.get_default_group_roles,
                related_name="groups",
                to="authentication.GroupRole",
                verbose_name="Tilgjengelige roller",
            ),
        ),
    ]