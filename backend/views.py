import mimetypes
from pathlib import Path

from django.conf import settings
from django.http import FileResponse, Http404


def flutter_web_app(request, path=''):
    """Serve Flutter assets and fall back to its single-page app entry point."""
    frontend_root = Path(settings.FRONTEND_ROOT).resolve()
    requested = (frontend_root / path).resolve() if path else frontend_root / 'index.html'

    if frontend_root not in requested.parents and requested != frontend_root:
        raise Http404

    asset = requested if requested.is_file() else frontend_root / 'index.html'
    if not asset.is_file():
        raise Http404('The admin web application has not been built yet.')

    content_type, encoding = mimetypes.guess_type(asset.name)
    response = FileResponse(asset.open('rb'), content_type=content_type or 'application/octet-stream')
    if encoding:
        response['Content-Encoding'] = encoding
    response['Cache-Control'] = (
        'no-cache' if asset.name == 'index.html' else 'public, max-age=31536000, immutable'
    )
    return response
