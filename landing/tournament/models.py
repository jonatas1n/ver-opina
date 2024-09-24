from django.db import models
from django.utils import timezone

from wagtail.models import Page


class Tournament(Page):
    tournament_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    competitions = models.ManyToManyField("tournament.Competition", related_name="tournament_competitions")  
    vote_interval = models.DurationField()

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
            
            results[competition.candidate_a.id] = {
                "data": competition.candidate_a,
                "votes": votes.filter(candidate_option=competition.candidate_a).count()
            }
            results[competition.candidate_b.id] = {
                "data": competition.candidate_b,
                "votes": votes.filter(candidate_option=competition.candidate_b).count()
            }
        return results


class Competition(models.Model):
    competition_name = models.CharField(max_length=255)
    candidate_a = models.ForeignKey('candidate.CandidatePage', on_delete=models.CASCADE, related_name='candidate_a')
    candidate_b = models.ForeignKey('candidate.CandidatePage', on_delete=models.CASCADE, related_name='candidate_b')
    tournament = models.ForeignKey('tournament.Tournament', on_delete=models.CASCADE, related_name='competition_tournaments')

    def __str__(self):
        return self.competition_name


class CompetitionVote(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    candidate_option = models.ForeignKey('candidate.CandidatePage', on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def verify_vote(self):
        is_on_time = self.competition.tournament.start_date <= self.created_at <= self.competition.tournament.end_date
        duration = self.competition.tournament.vote_interval
        last_ip_vote = CompetitionVote.objects.filter(ip_address=self.ip_address, created_at__gte=timezone.now() - duration).first()
        return is_on_time and not last_ip_vote

    def __str__(self):
        return f"{self.competition} - {self.candidate}"
