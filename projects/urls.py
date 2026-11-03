from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BookingRequestViewSet,
    ContentBlockViewSet,
    ProjectViewSet,
    ContactMessageViewSet,
    FAQViewSet,
    SiteSettingsView,
    AdminNotificationViewSet,
    DeviceTokenViewSet,
)

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'contacts', ContactMessageViewSet)
router.register(r'faqs', FAQViewSet)
router.register(r'bookings', BookingRequestViewSet)
router.register(r'content', ContentBlockViewSet)
router.register(r'notifications', AdminNotificationViewSet)
router.register(r'device-tokens', DeviceTokenViewSet)

urlpatterns = [
    path('settings/', SiteSettingsView.as_view(), name='site-settings'),
    path('', include(router.urls)),
]
