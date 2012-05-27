from django.templatetags.static import static
from django.utils.safestring import mark_safe
from mptt.templatetags.mptt_tags import register


@register.filter
def flag(country):
    url = static('geo/flags/%s.gif' % country.iso_code.lower())
    return mark_safe('<img src="%s">' % url)
