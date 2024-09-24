from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from candidate.models import Candidate

class CandidateAdmin(ModelAdmin):
    model = Candidate
    menu_label = "Candidatos"
    menu_icon = "list-ul"
    add_to_settings_menu = False
    exclude_from_explorer = True
    list_display = ("candidate_name", "election_id", "party", "image")
    search_fields = ("candidate_name", "election_id")

modeladmin_register(CandidateAdmin)
