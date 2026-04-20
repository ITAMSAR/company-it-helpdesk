from django import template

register = template.Library()

@register.filter
def split(value, delimiter):
    """Split string by delimiter"""
    if value:
        return value.split(delimiter)
    return []

@register.filter
def parse_specs(value):
    """Parse specifications text into list"""
    if not value:
        return []
    
    # Split by line breaks and filter empty lines
    lines = []
    for line in value.replace('\r\n', '\n').split('\n'):
        line = line.strip()
        if line:
            lines.append(line)
    
    return lines