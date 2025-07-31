from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.connections.models import ConnectionRequests
from apps.connections.tasks import connection_notification

@receiver(post_save, sender=ConnectionRequests)
def notify_on_save(sender, instance, created, **kwargs):
    if created:
        connection_notification.delay(instance.id, action='created')
    else:
        connection_notification.delay(instance.id, action='updated')