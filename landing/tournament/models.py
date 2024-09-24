from django.db import models
from django.utils import timezone

from wagtail.models import Page, ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel
from modelcluster.fields import ParentalKey


class Tournament(Page, ClusterableModel):
    parent_page_types = ['home.LandingPage']

    start_date = models.DateField(verbose_name="Data de início")
    end_date = models.DateField(verbose_name="Data de término")
    vote_interval = models.IntegerField(verbose_name="Intervalo entre os votos (em minutos)", default=15)

    content_panels = Page.content_panels + [
        FieldPanel("start_date"),
        FieldPanel("end_date"),
        FieldPanel("vote_interval"),
        InlinePanel("competitions", label="Competições")
    ]

    @staticmethod
    def active_tournament():
        tournament = Tournament.objects.filter(start_date__lte=timezone.now(), end_date__gte=timezone.now()).first()
        if not tournament:
            return None
        return tournament

    @property
    def get_results(self):
        if self.end_date > timezone.now():
            return None
        
        results = {}
        for competition in self.competitions.all():
            votes = CompetitionVote.objects.filter(competition=competition)

            for candidate in [competition.candidate_a, competition.candidate_b]:
                results[candidate.id] = {
                    "data": candidate,
                    "votes": 0
                }

        return results


class Competition(models.Model):
    candidate_a = models.ForeignKey('candidate.Candidate', on_delete=models.CASCADE, related_name='candidate_a')
    candidate_b = models.ForeignKey('candidate.Candidate', on_delete=models.CASCADE, related_name='candidate_b')
    tournament = ParentalKey('tournament.Tournament', on_delete=models.CASCADE, related_name='competitions')

    def __str__(self):
        return self.competition_name


class CompetitionVote(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    candidate_option = models.ForeignKey('candidate.Candidate', on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def verify_vote(self):
        is_on_time = self.competition.tournament.start_date <= self.created_at <= self.competition.tournament.end_date
        duration = self.competition.tournament.vote_interval
        last_ip_vote = CompetitionVote.objects.filter(ip_address=self.ip_address, created_at__gte=timezone.now() - duration).first()
        return is_on_time and not last_ip_vote

    def __str__(self):
        return f"{self.competition} - {self.candidate}"
