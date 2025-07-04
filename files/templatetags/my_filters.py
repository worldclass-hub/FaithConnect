from django import template
import re

register = template.Library()

@register.filter
def in_list(value, the_list):
    """
    Check if a value (like file extension) exists in a comma-separated list.
    Handles casing and spaces.
    Usage: {{ file.file_extension|in_list:".mp3,.wav,.aac" }}
    """
    if not value:
        return False
    ext_list = [x.strip().lower() for x in the_list.split(',')]
    return value.lower().strip() in ext_list


@register.filter
def youtube_id(value):
    """
    Extract YouTube video ID from various YouTube URL formats.
    """
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11})',  # standard formats
    ]

    for pattern in patterns:
        match = re.search(pattern, value)
        if match:
            return match.group(1)
    return value


@register.filter
def has_file(uploaded_file):
    """
    Check if a file exists and has a name (used for legacy FileField logic).
    """
    try:
        return bool(uploaded_file and uploaded_file.name)
    except ValueError:
        return False
