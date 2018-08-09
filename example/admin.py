from advanced_search.admin import BaseAdvacedSearchAdmin
from django.contrib.admin import register
from .form import AreaForm, AreaSearchForm
from .models import Area

@register(Area)
class AreaAdmin(BaseAdvacedSearchAdmin):
    form = AreaForm
    search_form = AreaSearchForm