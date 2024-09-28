from django.shortcuts import render, redirect
from tournament.forms import VoteForm
from tournament.models import Tournament
from django.utils import timezone


def index(request):
    active_tournament = Tournament.active_tournament()
    if not active_tournament:
        last_tournament = Tournament.objects.order_by("-end_date").first()
        last_results = last_tournament.get_results if last_tournament else None
        next_tournament = (
            Tournament.objects.filter(start_date__gte=timezone.localtime())
            .order_by("start_date")
            .first()
        )
        data = {
            "last_tournament": last_tournament,
            "last_results": last_results,
            "next_tournament": next_tournament,
        }
        return render(request, "tournament/no_tournament.html", data)

    if request.method == "GET":
        if not active_tournament.can_vote(request):
            print("Not on time")
            return redirect("/result")
        form = VoteForm(active_tournament.competitions.all())
        return render(
            request,
            "tournament/index.html",
            {"tournament": active_tournament, "form": form},
        )

    form = VoteForm(active_tournament.competitions.all(), request.POST)
    if form.is_valid() and active_tournament.can_vote(request):
        form.save(request)
        return redirect("/result")

    return render(
        request,
        "tournament/index.html",
        {"tournament": active_tournament, "form": form, "errors": form.errors},
    )


def result(request):
    active_tournament = Tournament.active_tournament()
    if not active_tournament:
        print("No active tournament")
        return redirect("/")

    can_vote = active_tournament.can_vote(request)
    remaining_time = active_tournament.start_date - timezone.localtime()
    remaining_time = remaining_time.total_seconds()
    results = active_tournament.get_results
    return render(
        request,
        "tournament/result.html",
        {
            "tournament": active_tournament,
            "results": results,
            "can_vote": can_vote,
            "remaining_time": remaining_time,
        },
    )
