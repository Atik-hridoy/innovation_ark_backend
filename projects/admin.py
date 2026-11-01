from django.contrib import admin
from .models import (
    BookingRequest,
    ContentBlock,
    ContactMessage,
    FAQ,
    Project,
    ProjectImage,
    SiteSettings,
)

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'sort_order', 'is_published', 'created_at')
    list_filter = ('is_published',)
    search_fields = ('title', 'subtitle', 'description', 'problem', 'solution', 'impact')
    inlines = [ProjectImageInline]

admin.site.register([ContactMessage, FAQ, SiteSettings, BookingRequest, ContentBlock, ProjectImage])
