from django.shortcuts import render
from django.shortcuts import redirect
from .forms import VoteForm

def index(request):
    from .models import Tournament, TournamentPage

    active_tournament = TournamentPage.active_tournament()
    if not active_tournament:
        last_tournament = Tournament.objects.order_by("-end_date").first()
        last_results = last_tournament.get_results if last_tournament else None
        data = {
            "last_tournament": last_tournament,
            "last_results": last_results
        }
        return render(request, "tournament/no_tournament.html", data)
    
    if request.method == "GET":
        form = VoteForm(active_tournament.competitions.all())
        return render(request, "tournament/index.html", {"tournament": active_tournament, "form": form})
    
    form = VoteForm(active_tournament.competitions.all(), request.POST)
    if form.is_valid():
        form.save()
        return redirect("/result")
    
    return render(request, "tournament/index.html", {"tournament": active_tournament, "form": form, "errors": form.errors})

def result(request):
    from .models import TournamentPage

    active_tournament = TournamentPage.active_tournament()
    if not active_tournament:
        return redirect("/")
    
    results = active_tournament.get_results
    return render(request, "tournament/result.html", {"tournament": active_tournament, "results": results})
