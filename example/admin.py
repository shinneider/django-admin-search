from django_admin_search.admin import BaseAdvacedSearchAdmin
from django.contrib.admin import register
from .form import AreaForm, AreaSearchForm
from .models import Area

@register(Area)
class AreaAdmin(BaseAdvacedSearchAdmin):
    form = AreaForm
    search_form = AreaSearchForm


    # you need intercept a search query for specific field ? try this:
    # def search_YouFormFieldHere(request, field_value, get_values):
    #   query = Q()
    #   ...
    #   return query