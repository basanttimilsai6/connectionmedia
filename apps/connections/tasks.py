from celery import shared_task
from apps.notifications.models import Notification
from apps.connections.models import ConnectionRequests
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist


@shared_task
def connection_notification(request_id, action='updated'):
    try:
        request = (
            ConnectionRequests.objects
            .select_related('sender', 'receiver')
            .get(id=request_id)
        )
    except ObjectDoesNotExist:
        return

    sender = request.sender
    receiver = request.receiver
    status = request.status.lower()

    if action == 'created':
        # ensure both notifications are saved together
        with transaction.atomic():
            Notification.objects.create(
                user=receiver,
                message=f"{sender.full_name} sent you a connection request."
            )
            Notification.objects.create(
                user=sender,
                message=f"Your connection request was {status} by {receiver.full_name}."
            )

    elif action == 'updated':
        Notification.objects.create(
            user=sender,
            message=f"Your connection request was {status} by {receiver.full_name}."
        )