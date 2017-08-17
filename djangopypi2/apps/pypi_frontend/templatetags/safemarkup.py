#######################
from __future__ import unicode_literals, print_function
#######################
from django import template
from django.conf import settings
from django.utils.encoding import smart_str, force_text
from django.utils.safestring import mark_safe

register = template.Library()


def saferst(value):
    try:
        from docutils.core import publish_parts
    except ImportError:
        return force_text(value)

    docutils_settings = getattr(settings, "RESTRUCTUREDTEXT_FILTER_SETTINGS",
                                dict())
    
    try:
        parts = publish_parts(source=smart_str(value),
                              writer_name="html4css1",
                              settings_overrides=docutils_settings)
    except:
        return force_text(value)
    else:
        return mark_safe(force_text(parts["fragment"]))
saferst.is_safe = True
register.filter(saferst)

