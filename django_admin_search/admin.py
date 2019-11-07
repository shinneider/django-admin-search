# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.admin import ModelAdmin
from django.contrib.admin.views.main import ChangeList
from django.db.models import Q

from django_admin_search import utils as u

class AdvancedSearchChangeList(ChangeList):
    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.full_params = None

    def get_query_string(self, *args, **kwargs):
        self.params, self.full_params = self.full_params, self.params
        result = super().get_query_string(*args, **kwargs)
        self.params, self.full_params = self.full_params, self.params
        return result

class AdvancedSearchAdmin(ModelAdmin):
    """
        class to add custom filters in django admin
    """
    change_list_template = 'admin/custom_change_list.html'
    advanced_search_fields = {}

    def get_changelist(self, request):
        return AdvancedSearchChangeList

    def get_changelist_instance(self, request):
        """
        prevent error by removing advanced search params from GET params
        """
        get_copy = request.GET.copy()
        request.GET._mutable = True
        self.extract_advanced_search_terms(request.GET)
        request.GET._mutable = False
        r = super().get_changelist_instance(request)
        r.full_params = dict(get_copy.items())
        request.GET = get_copy
        return r

    def lookup_allowed(self, lookup, value):
        """
            override django admin 'lookup_allowed'
        """
        if lookup in self.advanced_search_form().fields.keys():
            return True
        return super().lookup_allowed(lookup, value)

    def get_queryset(self, request):
        """
            override django admin 'get_queryset'
        """
        qs = super().get_queryset(request)
        return self.advanced_search(request, qs)

    def changelist_view(self, request, extra_context=None):
        advanced_search_form = self.extract_advanced_search_terms(dict(request.GET.items()))
        extra_context = {'asf': advanced_search_form}
        return super().changelist_view(request, extra_context=extra_context)

    def advanced_search(self, request, qs):
        qs = qs.filter(self.advanced_search_query(request, Q(), self.advanced_search_fields))
        self.advanced_search_fields = {}  # Clear CACHED Get values
        return qs

    def advanced_search_form(self, request=None):
        if hasattr(self, 'search_form'):
            return self.search_form(data=request)

        return None
    
    def extract_advanced_search_terms(self, param_dict):
        advanced_search_form = self.advanced_search_form(param_dict)
        if advanced_search_form is not None:
            for key in advanced_search_form.fields.keys():
                temp = param_dict.pop(key, None)
                if temp:  # there is a field but it's empty so it's useless
                    self.advanced_search_fields[key] = temp
        return advanced_search_form

    def advanced_search_query(self, request, query, param_values):
        """
            Get form and mount filter query if form is not none
        """
        form = self.advanced_search_form()
        if form is None:
            return query

        for field, form_field in self.advanced_search_form().fields.items():
            field_value = param_values[field][0] if field in param_values else None

            # to overide default filter for a sigle field
            if hasattr(self, ('search_' + field)):
                query &= getattr(self, 'search_' + field)(field, field_value,
                                                          form_field, request,
                                                          param_values)
                continue

            if field_value in [None, '']:
                continue

            field_name = form_field.widget.attrs.get('filter_field', field)
            field_filter = field_name + form_field.widget.attrs.get('filter_method', '')

            try:
                field_value = u.format_data(form_field, field_value)  # format by field type
                query &= Q(**{field_filter: field_value})
            except:
                continue

        return query
