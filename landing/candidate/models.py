from django.db import models


class Candidate(models.Model):
    candidate_name = models.CharField(max_length=255)
    election_id = models.CharField()
    party = models.ForeignKey("candidate.Party", on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return f"{self.candidate_name} - {self.election_id}"

    class Meta:
        verbose_name = "Candidato"
        verbose_name_plural = "Candidatos"

class Party(models.Model):
    party_name = models.CharField(max_length=255)
    party_logo = models.ImageField(null=True, blank=True)
    party_description = models.TextField()

    def __str__(self):
        return self.party_name
    class Meta:
        verbose_name = "Partido"
        verbose_name_plural = "Partidos"
