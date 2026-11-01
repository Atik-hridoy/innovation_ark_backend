from rest_framework import serializers
import json
from .models import (
    BookingRequest,
    ContentBlock,
    Project,
    ProjectImage,
    ContactMessage,
    FAQ,
    SiteSettings,
)

class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = '__all__'


class ProjectImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProjectImage
        fields = ('id', 'image', 'image_url', 'caption', 'order', 'created_at')

    def get_image_url(self, obj):
        if not obj.image:
            return None
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url


class ProjectSerializer(serializers.ModelSerializer):
    images = ProjectImageSerializer(many=True, read_only=True)
    mockups = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'

    def get_mockups(self, obj):
        request = self.context.get('request')

        def build_url(img_field):
            if not img_field:
                return None
            try:
                url = img_field.url
                if request and not url.startswith('http'):
                    return request.build_absolute_uri(url)
                return url
            except Exception:
                return None

        urls = []
        for img in obj.images.all():
            u = build_url(img.image)
            if u and u not in urls:
                urls.append(u)

        for m in (obj.mockup_1, obj.mockup_2, obj.mockup_3, obj.mockup_4):
            u = build_url(m)
            if u and u not in urls:
                urls.append(u)

        return urls

    def to_internal_value(self, data):
        internal_data = super().to_internal_value(data)
        if 'tags' in data:
            val = data['tags']
            if isinstance(val, str):
                try:
                    internal_data['tags'] = json.loads(val)
                except Exception:
                    internal_data['tags'] = [
                        t.strip() for t in val.split(',') if t.strip()
                    ]
            elif isinstance(val, list):
                internal_data['tags'] = val
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
