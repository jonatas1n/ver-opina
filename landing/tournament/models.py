from django.db import models
from django.utils import timezone

from wagtail.models import Page, ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel
from modelcluster.fields import ParentalKey


class Tournament(ClusterableModel):
    class Meta:
        verbose_name = "Torneio"
        verbose_name_plural = "Torneios"

    parent_page_types = ["home.LandingPage"]

    start_date = models.DateTimeField(verbose_name="Data de início")
    end_date = models.DateTimeField(verbose_name="Data de término")
    vote_interval = models.IntegerField(
        verbose_name="Intervalo entre os votos (em minutos)", default=15
    )

    @staticmethod
    def active_tournament():
        tournament = Tournament.objects.filter(
            start_date__lte=timezone.localtime(), end_date__gte=timezone.localtime()
        ).first()
        if not tournament:
            return None
        return tournament

    def is_on_time(self, time=timezone.localtime()):
        start_date = timezone.localtime(self.start_date)
        end_date = timezone.localtime(self.end_date)
        return start_date <= time <= end_date

    def can_vote(self, request):
        if not self.is_on_time():
            print("Not on time")
            return False
        access_ip = request.META.get("REMOTE_ADDR")
        last_vote = CompetitionVote.objects.filter(
            ip_address=access_ip,
            created_at__gte=timezone.localtime()
            - timezone.timedelta(minutes=self.vote_interval),
        ).first()
        return last_vote is None

    @property
    def get_results(self):
        timezone.localtime()
        if self.start_date > timezone.localtime():
            return None

        results = []
        for competition in self.competitions.all():
            votes = CompetitionVote.objects.filter(competition=competition)

            competition_turn = []

            for candidate in [competition.candidate_a, competition.candidate_b]:
                percentage = (
                    votes.filter(candidate_option=candidate).count() / votes.count()
                    if votes.count()
                    else 0
                )
                percentage = round(percentage * 100, 2)
                competition_turn.append(
                    {
                        "data": candidate,
                        "votes": votes.filter(candidate_option=candidate).count(),
                        "percentage": percentage,
                    }
                )

            results.append(competition_turn)

        return results


class Competition(models.Model):
    candidate_a = models.ForeignKey(
        "candidate.Candidate", on_delete=models.CASCADE, related_name="candidate_a"
    )
    candidate_b = models.ForeignKey(
        "candidate.Candidate", on_delete=models.CASCADE, related_name="candidate_b"
    )
    tournament = ParentalKey(
        "tournament.Tournament", on_delete=models.CASCADE, related_name="competitions"
    )

    def __str__(self):
        candidate_a = self.candidate_a.name
        candidate_b = self.candidate_b.name
        return f"{candidate_a} x {candidate_b}"


class CompetitionVote(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    candidate_option = models.ForeignKey(
        "candidate.Candidate", on_delete=models.CASCADE
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.competition} - {self.ip_address}"
