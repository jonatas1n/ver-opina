from django.core.management.base import BaseCommand
from candidate.models import Candidate, Party

from candidate.crawler import crawler

class Command(BaseCommand):
    help = "Extracts the data from the database and saves it to a file"

    def handle(self, *args, **options):
        candidates = crawler()
        print(f"Total de candidatos: {len(candidates)}")

        for candidate in candidates:
            party = candidate.pop('nomeColigacao')
            party, was_created = Party.objects.get_or_create(party_name=party)
            if was_created:
                print(f"Partido criado: {party}")
            candidate['party'] = party
            Candidate.objects.get_or_create(**candidate)
