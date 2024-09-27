from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.admin.panels import FieldPanel, InlinePanel
from tournament.models import Tournament, Competition

class CompetitionInlinePanel(InlinePanel):
    model = Competition
    panels = [
        FieldPanel("candidate_a"),
        FieldPanel("candidate_b"),
    ]

class TournamentAdmin(ModelAdmin):
    model = Tournament
    menu_label = "Torneios"
    menu_icon = "list-ul"
    add_to_settings_menu = False
    exclude_from_explorer = True
    list_display = ("start_date", "end_date", "vote_interval")
    search_fields = ("start_date", "end_date")
    panels = [
        FieldPanel("start_date"),
        FieldPanel("end_date"),
        FieldPanel("vote_interval"),
        InlinePanel("competitions", label="Competições"),
    ]

modeladmin_register(TournamentAdmin)
