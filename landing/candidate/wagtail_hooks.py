from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from candidate.models import Candidate


class CandidateAdmin(ModelAdmin):
    model = Candidate
    menu_label = "Candidatos"
    menu_icon = "list-ul"
    add_to_settings_menu = False
    exclude_from_explorer = True
    list_display = ("name", "number", "party")
    search_fields = ("name", "number")


modeladmin_register(CandidateAdmin)
