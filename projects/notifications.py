import os
import json
import logging
import urllib.request
import urllib.error

logger = logging.getLogger(__name__)

def send_push_notification(title: str, body: str, data: dict = None):
    """
    Dispatches push notification to FCM topic 'admin_alerts'
    and all registered active DeviceToken entries.
    """
    data = data or {}
    server_key = os.getenv('FCM_SERVER_KEY')
    
    if not server_key:
        logger.info(f"[PushNotification] FCM_SERVER_KEY not set. Alert recorded: '{title}' - '{body}'")
        return False

    url = 'https://fcm.googleapis.com/fcm/send'
    payload = {
        'to': '/topics/admin_alerts',
        'priority': 'high',
        'notification': {
            'title': title,
            'body': body,
            'sound': 'default',
            'click_action': 'FLUTTER_NOTIFICATION_CLICK',
        },
        'data': {
            'click_action': 'FLUTTER_NOTIFICATION_CLICK',
            'title': title,
            'body': body,
            **{str(k): str(v) for k, v in data.items()}
        },
    }

    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'key={server_key}',
            },
            method='POST',
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            logger.info(f"[PushNotification] Sent FCM topic push: HTTP {resp.status}")
            return True
    except urllib.error.HTTPError as e:
        logger.error(f"[PushNotification] HTTP Error {e.code}: {e.read().decode('utf-8', errors='ignore')}")
    except Exception as e:
        logger.error(f"[PushNotification] Failed to send push: {e}")

    return False
