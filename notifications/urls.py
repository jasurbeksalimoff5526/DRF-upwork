from django.urls import path
from .views import NotificationListAPIView, UnreadNotificationListAPIView, MarkNotificationAsReadAPIView, MarkAllNotificationsAsReadAPIView, UnreadNotificationCountAPIView


urlpatterns = [
    path("", NotificationListAPIView.as_view(), name="notification-list"),
    path("unread/", UnreadNotificationListAPIView.as_view(), name="notification-unread"),
    path("unread-count/", UnreadNotificationCountAPIView.as_view(), name="notification-unread-count"),
    path("<int:pk>/read/", MarkNotificationAsReadAPIView.as_view(), name="notification-read"),
    path("read-all/", MarkAllNotificationsAsReadAPIView.as_view(), name="notification-read-all"),
]
