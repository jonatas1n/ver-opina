from tabnanny import verbose
from django.db import models


class Candidate(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nome do Candidato")
    nick = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Nome de Urna"
    )
    election_id = models.CharField(
        verbose_name="ID do candidato na Eleição", max_length=255, null=True, blank=True
    )
    party = models.ForeignKey(
        "candidate.Party",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Partido",
    )
    image_url = models.URLField(null=True, blank=True)
    site_id = models.CharField(max_length=255, null=True, blank=True)
    number = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Número da Eleição"
    )
    municipio_id = models.CharField(max_length=255, null=True, blank=True)
    municipio = models.CharField(max_length=255, null=True, blank=True)
    region = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Região"
    )
    year = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Ano da Eleição"
    )
    uf = models.CharField(max_length=255, null=True, blank=True, verbose_name="UF")

    @property
    def url(self):
        url = (
            "https://divulgacandcontas.tse.jus.br/divulga/#/candidato/{}/{}/{}/{}/{}/{}"
        )
        return url.format(
            self.region, self.uf, self.year, self.site_id, self.year, self.municipio_id
        )

    def __str__(self):
        return f"{self.name} - {self.number}"

    class Meta:
        verbose_name = "Candidato"
        verbose_name_plural = "Candidatos"


class Party(models.Model):
    party_name = models.CharField(max_length=255)
    party_logo = models.ImageField(null=True, blank=True)
    party_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.party_name

    class Meta:
        verbose_name = "Partido"
        verbose_name_plural = "Partidos"
