from django.db import models

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel

class TournamentPage(Page):
    tournament_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    competitions = models.ManyToManyField("tournament.Competition")

    content_panels = Page.content_panels + [
        FieldPanel("tournament_name"),
        FieldPanel("start_date"),
        FieldPanel("end_date"),
        FieldPanel("competitions"),
    ]

class Competition(models.Model):
    competition_name = models.CharField(max_length=255)
    candidate_a = models.ForeignKey('candidate.CandidatePage', on_delete=models.CASCADE, related_name='candidate_a')
    candidate_b = models.ForeignKey('candidate.CandidatePage', on_delete=models.CASCADE, related_name='candidate_b')
    tournament = models.ForeignKey(TournamentPage, on_delete=models.CASCADE)

    def __str__(self):
        return self.competition_name
