# -*- coding: utf-8 -*-
from django.contrib.admin import ModelAdmin
from django.db.models import Q
from django_admin_search import utils as u
from django.contrib import messages


class BaseAdvacedSearchAdmin(ModelAdmin):
    change_list_template = 'admin/custom_change_list.html'
    advanced_search_fields = {}
    
    def lookup_allowed(self, lookup):
        if lookup in self.advanced_search_form().fields.keys():
            return True
        return super(BaseAdvacedSearchAdmin, self).lookup_allowed(lookup)
    
    def get_queryset(self, request):
        qs = super(BaseAdvacedSearchAdmin, self).get_queryset(request)
        return self.advanced_search(request, qs)

    def changelist_view(self, request, extra_context=None, **kwargs):
        advanced_search_form = self.advanced_search_form(request.GET)
        extra_context = {'asf':advanced_search_form}
        
        if advanced_search_form is not None:
            request.GET._mutable=True
            for key in advanced_search_form.fields.keys():
                try:
                    temp = request.GET.pop(key)
                except KeyError:
                    pass # there is no field of the form in the dict so we don't remove it
                else:
                    if temp!=['']: #there is a field but it's empty so it's useless
                        self.advanced_search_fields[key] = temp 
            request.GET_mutable=False
        
        return super(BaseAdvacedSearchAdmin, self).changelist_view(request, extra_context=extra_context)

    def advanced_search(self, request, qs):
        qs = qs.filter(self.advanced_search_query(request, Q(), self.advanced_search_fields))
        
        # Clear CACHED Get values
        self.advanced_search_fields = {}

        return qs
    
    def advanced_search_form(self, request=None):
        if hasattr(self, 'search_form'):
            return self.search_form(data=request)
        
        return None

    def advanced_search_query(self, request, query, get_values):
        """
        Get form and mount filter query if form is not none
        """
        form = self.advanced_search_form()
        if form is None:
            return query

        for key, value in self.advanced_search_form().fields.items():
            key_value = get_values[key][0] if key in get_values else None

            # to overide default filter for a sigle field
            if hasattr(self, ('search_' + key)):
                query &= getattr(self, 'search_' + key)(request, key_value, get_values)
                continue

            if key_value is None:
                continue

            key = value.widget.attrs.get('filter_field', key)
            field_query = key + value.widget.attrs.get('filter_method', '')

            try:
                key_value = u.format_data(value, key_value)
                query &= Q(**{field_query: key_value})
            except:
                continue

        return query