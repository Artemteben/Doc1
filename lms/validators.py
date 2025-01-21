from django.core.exceptions import ValidationError
from urllib.parse import urlparse


def youtube_only_validator(value):
    parsed_url = urlparse(value)
    if parsed_url.netloc not in ["www.youtube.com", "youtube.com"]:
        raise ValidationError("Only YouTube links are allowed.")
