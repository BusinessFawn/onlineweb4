import json
import logging

from django.conf import settings
from django.core.mail import send_mail
from onlineweb4.celery import app as celery_app
from pywebpush import WebPushException, webpush
from rest_framework import serializers

from .constants import (
    NOTIFICATION_BADGE_URL,
    NOTIFICATION_SOUND,
    NOTIFICATION_VIBRATION_PATTERN,
)
from .models import Notification

logger = logging.getLogger(__name__)

VAPID_PRIVATE_KEY = settings.OW4_VAPID_PRIVATE_KEY_PATH

VAPID_CLAIMS = {
    "sub": "mailto:dotkom@online.ntnu.no",
}


def _send_webpush(subscription_info: dict, data: dict) -> bool:
    """
    Send a webpush message asynchronously
    """

    json_data = json.dumps(data)

    try:
        webpush(
            subscription_info=subscription_info,
            data=json_data,
            vapid_private_key=VAPID_PRIVATE_KEY,
            vapid_claims=VAPID_CLAIMS,
        )
        return True
    except WebPushException as error:
        logger.error(error)
        # Mozilla returns additional information in the body of the response.
        if error.response and error.response.json():
            logger.error(error.response.json())
        return False
    except TypeError as error:
        logger.error(error)
        raise error


class NotificationDataSerializer(serializers.ModelSerializer):
    badge = NOTIFICATION_BADGE_URL
    vibrate = NOTIFICATION_VIBRATION_PATTERN
    sound = NOTIFICATION_SOUND

    timestamp = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_timestamp(self, obj: Notification):
        return obj.created_date.timestamp()

    def get_image(self, obj: Notification):
        if obj.image:
            return obj.image.md
        return None

    class Meta:
        model = Notification
        fields = (
            "badge",
            "vibrate",
            "sound",
            "image",
            "icon",
            "title",
            "body",
            "tag",
            "require_interaction",
            "renotify",
            "silent",
            "timestamp",
            "url",
        )


@celery_app.task(bind=True)
def dispatch_push_notification_task(_, notification_id: int):
    notification = Notification.objects.get(pk=notification_id)
    user = notification.recipient
    notification_data = NotificationDataSerializer(notification).data

    results = []
    for subscription in user.notification_subscriptions.all():
        subscription_info = subscription.to_vapid_format()
        result = _send_webpush(subscription_info, data=notification_data)
        results.append(result)

    did_any_message_succeed = any(results)
    notification.sent_push = did_any_message_succeed
    notification.save()


@celery_app.task(bind=True)
def dispatch_email_notification_task(_, notification_id: int):
    notification = Notification.objects.get(pk=notification_id)
    user = notification.recipient

    send_mail(
        subject=notification.title,
        message=notification.body,
        from_email=notification.from_mail,
        recipient_list=[user.primary_email],
        fail_silently=False,
    )

    notification.sent_email = True
    notification.save()