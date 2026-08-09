from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, ContactMessageViewSet, FAQViewSet, SiteSettingsView

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'contacts', ContactMessageViewSet)
router.register(r'faqs', FAQViewSet)

urlpatterns = [
    path('settings/', SiteSettingsView.as_view(), name='site-settings'),
    path('', include(router.urls)),
]
