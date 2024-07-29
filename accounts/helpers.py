import uuid
import hmac
import hashlib
import base64

from django.urls import reverse


def calc_tracking_number():
    return uuid.uuid4().hex


def generate_hmac_signature(secret_key, message):
    hmac_obj = hmac.new(secret_key.encode(), message.encode(), hashlib.sha256)
    hmac_signature = hmac_obj.digest()
    signature = base64.b64encode(hmac_signature).decode()

    return signature


def build_abs_uri(request, url_name, *args):
    return request.build_absolute_uri(reverse(url_name, args=args))
