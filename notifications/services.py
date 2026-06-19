from .models import Notification


def create_notification(
    *,
    receiver,
    notification_type,
    title,
    message,
    actor=None,
    project=None,
    contract=None
):
    return Notification.objects.create(
        receiver=receiver,
        actor=actor,
        notification_type=notification_type,
        title=title,
        message=message,
        project=project,
        contract=contract,
        is_read=False
    )



