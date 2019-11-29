from django.contrib.admin import register
from django.db.models import Q

from django_admin_search.admin import AdvancedSearchAdmin

from .form import AreaForm, AreaSearchForm
from .models import Area


@register(Area)
class AreaAdmin(AdvancedSearchAdmin):
    form = AreaForm
    search_form = AreaSearchForm

    def search_description(self, field, field_value, form_field, request, param_values):
        """
            intercept query filter for description field
        """
        query = Q()
        # your Q logic here
        return query
