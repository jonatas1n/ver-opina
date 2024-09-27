from wagtail.models import Page
from django.db import models

from wagtail.admin.panels import FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, path, route

from django.utils import timezone
from tournament.models import Tournament

from home.views import index, result


class LandingPage(RoutablePageMixin, Page):
    max_count = 1
    is_creatable = True

    heading = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        verbose_name="Título",
    )

    subheading = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        verbose_name="Subtítulo",
    )

    content_panels = Page.content_panels + [
        FieldPanel("heading"),
        FieldPanel("subheading"),
    ]

    @route(r"^$")
    def index(self, request):
        return index(request)

    @path("result/")
    def result(self, request):
        return result(request)

    @property
    def actual_tournament(self):
        active_tournament = Tournament.active_tournament()
        if not active_tournament:
            return None
        return active_tournament

    @property
    def last_result(self):
        last_tournament = (
            Tournament.objects.filter(end_date__lte=timezone.localtime())
            .order_by("-end_date")
            .first()
        )
        return last_tournament.get_results if last_tournament else None
