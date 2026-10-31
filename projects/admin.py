from django.contrib import admin
from .models import BookingRequest, ContentBlock, ContactMessage, FAQ, Project, SiteSettings

admin.site.register([Project, ContactMessage, FAQ, SiteSettings, BookingRequest, ContentBlock])

# Register your models here.
