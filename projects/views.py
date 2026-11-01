import json
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import (
    BookingRequest,
    ContentBlock,
    Project,
    ProjectImage,
    ContactMessage,
    FAQ,
    SiteSettings,
)
from .serializers import (
    BookingRequestSerializer,
    ContentBlockSerializer,
    ProjectSerializer,
    ProjectImageSerializer,
    ContactMessageSerializer,
    FAQSerializer,
    SiteSettingsSerializer,
)

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class SiteSettingsView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        settings = SiteSettings.load()
        serializer = SiteSettingsSerializer(settings, context={'request': request})
        return Response(serializer.data)

    def put(self, request):
        settings = SiteSettings.load()
        serializer = SiteSettingsSerializer(
            settings, data=request.data, partial=True, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('sort_order', '-created_at')
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminOrReadOnly]

    def _handle_images(self, project, request):
        # 1. Handle deleted images if requested
        delete_ids = request.data.get('delete_image_ids')
        if delete_ids:
            if isinstance(delete_ids, str):
                try:
                    delete_ids = json.loads(delete_ids)
                except Exception:
                    delete_ids = [
                        int(i.strip())
                        for i in delete_ids.split(',')
                        if i.strip().isdigit()
                    ]
            if isinstance(delete_ids, (list, tuple)):
                ProjectImage.objects.filter(project=project, id__in=delete_ids).delete()

        # 2. Handle multiple uploaded images (e.g. from 'images' or 'uploaded_images')
        new_files = request.FILES.getlist('images') or request.FILES.getlist(
            'uploaded_images'
        )
        if new_files:
            current_order = project.images.count()
            for idx, file_obj in enumerate(new_files):
                ProjectImage.objects.create(
                    project=project,
                    image=file_obj,
                    order=current_order + idx,
                )

    def perform_create(self, serializer):
        project = serializer.save()
        self._handle_images(project, self.request)

    def perform_update(self, serializer):
        project = serializer.save()
        self._handle_images(project, self.request)

    @action(detail=True, methods=['post'], url_path='delete-image')
    def delete_image(self, request, pk=None):
        project = self.get_object()
        image_id = request.data.get('image_id')
        if not image_id:
            return Response(
                {'error': 'image_id is required'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            img = project.images.get(id=image_id)
            img.delete()
            return Response({'status': 'deleted', 'id': image_id})
        except ProjectImage.DoesNotExist:
            return Response(
                {'error': 'Image not found in this project'},
                status=status.HTTP_404_NOT_FOUND,
            )


class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all().order_by('-created_at')
    serializer_class = ContactMessageSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [IsAdminOrReadOnly]


class BookingRequestViewSet(viewsets.ModelViewSet):
    queryset = BookingRequest.objects.all()
    serializer_class = BookingRequestSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class ContentBlockViewSet(viewsets.ModelViewSet):
    queryset = ContentBlock.objects.all()
    serializer_class = ContentBlockSerializer
    permission_classes = [IsAdminOrReadOnly]
