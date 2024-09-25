from django import template
from candidate.models import Candidate

register = template.Library()

@register.inclusion_tag("tags/candidate_card.html")
def candidate_card(candidate_option):
    print(candidate_option.data)
    candidate = candidate_option.data['label']
    return {
        "candidate": candidate
    }
