# Generated by Django 2.1.8 on 2019-05-12 13:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_registration', models.BooleanField(default=False)),
                ('event_changes', models.BooleanField(default=False)),
                ('event_waitlist_bump', models.BooleanField(default=False)),
                ('article_created', models.BooleanField(default=False)),
                ('offline_created', models.BooleanField(default=False)),
                ('general_updates', models.BooleanField(default=False)),
                ('wine_punishment_created', models.BooleanField(default=False)),
                ('unanswered_feedback', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notification_settings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NotificationSubscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('endpoint', models.URLField(max_length=500, unique=True)),
                ('auth', models.CharField(max_length=500, unique=True)),
                ('p256dh', models.CharField(max_length=500, unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notification_subscriptions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Pushvarslingsabbonement',
                'verbose_name_plural': 'Pushvarslingsabbonement',
            },
        ),
    ]