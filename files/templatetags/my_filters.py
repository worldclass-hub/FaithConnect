from django import template
import re

register = template.Library()

@register.filter
def in_list(value, the_list):
    return value in the_list.split(',')

@register.filter
def youtube_id(value):
    """
    Extracts the YouTube video ID from a URL.

    Returns the 11-character video ID or the original value if no match.
    """
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11})',
    ]

    for pattern in patterns:
        match = re.search(pattern, value)
        if match:
            return match.group(1)
    return value


@register.filter
def has_file(uploaded_file):
    try:
        return bool(uploaded_file and uploaded_file.name)
    except ValueError:
        return False
