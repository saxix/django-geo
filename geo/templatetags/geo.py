from django.templatetags.static import static
from django.utils.safestring import mark_safe
from mptt.templatetags.mptt_tags import register


@register.filter
def flag(country):
    code = country.iso_code.lower()
    url = static('geo/flags/%s.gif' % code)
    return mark_safe('<img width="16" height="11" id="%s_flag" src="%s">' % (code, url))
