from rest_framework import serializers
import json
from .models import BookingRequest, ContentBlock, Project, ContactMessage, FAQ, SiteSettings

class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

    def to_internal_value(self, data):
        # Handle tags which might come as a JSON string from FormData
        internal_data = super().to_internal_value(data)
        if 'tags' in data and isinstance(data['tags'], str):
            try:
                internal_data['tags'] = json.loads(data['tags'])
            except json.JSONDecodeError:
                pass
        return internal_data

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = '__all__'

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'


class BookingRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingRequest
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class ContentBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentBlock
        fields = '__all__'
        read_only_fields = ('updated_at',)
