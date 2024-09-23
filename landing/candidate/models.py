from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel


class CandidatePage(Page):
    candidate_name = models.CharField(max_length=255)
    election_id = models.CharField()
    party = models.CharField()
    image = models.ImageField()
    data = models.JSONField() # TODO: Figure the data structure for this field

    content_panels = Page.content_panels + [
        FieldPanel("candidate_name"),
        FieldPanel("election_id"),
        FieldPanel("party"),
        FieldPanel("data"),
    ]
