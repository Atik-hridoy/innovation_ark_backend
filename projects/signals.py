from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BookingRequest, ContactMessage, AdminNotification
from .notifications import send_push_notification

@receiver(post_save, sender=BookingRequest)
def on_booking_created(sender, instance, created, **kwargs):
    if created:
        title = "📅 New Consultation Booking!"
        body = f"{instance.name} requested {instance.project_type} on {instance.preferred_date} at {instance.preferred_time}"
        AdminNotification.objects.create(
            title=title,
            body=body,
            category='booking',
            reference_id=instance.id,
        )
        send_push_notification(
            title=title,
            body=body,
            data={
                'type': 'booking',
                'id': instance.id,
                'name': instance.name,
                'email': instance.email,
            }
        )

@receiver(post_save, sender=ContactMessage)
def on_contact_created(sender, instance, created, **kwargs):
    if created:
        title = "💬 New Contact Message!"
        body = f"{instance.name}: {instance.message[:90]}"
        AdminNotification.objects.create(
            title=title,
            body=body,
            category='contact',
            reference_id=instance.id,
        )
        send_push_notification(
            title=title,
            body=body,
            data={
                'type': 'contact',
                'id': instance.id,
                'name': instance.name,
                'email': instance.email,
            }
        )
