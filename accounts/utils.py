from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings


def send_verification_email(user, request):
    uid = urlsafe_base64_encode(force_bytes(user.id))
    token = default_token_generator.make_token(user)
    verify_url = f"{request.scheme}://{request.get_host()}/api/verify-email/{uid}/{token}/"

    subject = "Verify your email"
    message = f"Hi {user.get_full_name()},\n\nPlease verify your email by clicking the link below:\n\n{verify_url}\n\nThanks!"
    
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
