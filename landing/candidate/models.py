from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel


class CandidatePage(Page):
    candidate_name = models.CharField(max_length=255)
    election_id = models.CharField()
    party = models.ForeignKey("candidate.Party", on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("candidate_name"),
        FieldPanel("election_id"),
        FieldPanel("party"),
    ]

class Party(models.Model):
    party_name = models.CharField(max_length=255)
    party_logo = models.ImageField(null=True, blank=True)
    party_description = models.TextField()

    def __str__(self):
        return self.party_name
