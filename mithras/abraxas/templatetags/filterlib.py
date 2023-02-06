import markdown
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


def expand(e):
    if e == "codehilite":
        return "markdown.extensions.codehilite"
    return e


@register.filter(name="cmarkdown")
@stringfilter
def cmarkdown(value, arg=""):
    """
    Filter to create HTML out of Markdown, using custom extensions.

    The diffrence between this filter and the django-internal markdown
    filter (located in ``django/contrib/markup/templatetags/markup.py``)
    is that this filter enables extensions to be load.

    Usage::

        {{ object.text|cmarkdown:"codehilite" }}

    This code is taken from
    http://www.freewisdom.org/projects/python-markdown/Django
    """
    extensions = arg.split(",")
    expanded_extensions = [expand(e) for e in extensions]
    return markdown.markdown(value, extensions=expanded_extensions)
