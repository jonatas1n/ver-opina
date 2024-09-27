from django import template
from home.models import LandingPage

register = template.Library()


@register.inclusion_tag("tags/heading.html")
def heading():
    heading = LandingPage.objects.first().heading
    return {
        "heading": heading,
    }
