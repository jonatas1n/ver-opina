from django import template
from home.models import LandingPage

register = template.Library()


@register.inclusion_tag("tags/subheading.html")
def subheading():
    subheading = LandingPage.objects.first().subheading
    return {
        "subheading": subheading,
    }
