from django import template

register = template.Library()

@register.inclusion_tag("tags/results.html")
def results(title, competitions):
    return {
        "title": title,
        "competitions": competitions,
    }
