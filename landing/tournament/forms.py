from django import forms


class VoteForm(forms.Form):
    def __init__(self, competitions, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.competitions = competitions

        for competition in competitions:
            candidates = [
                (competition.candidate_a.id, competition.candidate_a),
                (competition.candidate_b.id, competition.candidate_b),
            ]
            self.fields[f"competition_{competition.id}"] = forms.ChoiceField(
                label=str(competition.id), choices=candidates, widget=forms.RadioSelect
            )

    def save(self, request):
        from tournament.models import CompetitionVote

        votes = []
        for competition in self.competitions:
            candidate_id = self.cleaned_data.get(f"competition_{competition.id}")
            user_ip = request.META.get("REMOTE_ADDR")
            vote = CompetitionVote(
                competition=competition, candidate_option_id=candidate_id, ip_address=user_ip
            )
            votes.append(vote)

        CompetitionVote.objects.bulk_create(votes)
        return votes
