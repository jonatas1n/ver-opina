from django import template

register = template.Library()

@register.inclusion_tag("tags/candidate_card.html")
def candidate_card(candidate_option):
    candidate = candidate_option.data['label']
    name = candidate_option.data['name']
    return {
        "candidate": candidate,
        "name": name,
        "value": candidate_option.data['value']
    }
