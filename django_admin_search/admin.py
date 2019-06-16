# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.admin import ModelAdmin
from django.db.models import Q

from django_admin_search import utils as u


class AdvacedSearchAdmin(ModelAdmin):
    """
        class to add custom filters in django admin
    """
    change_list_template = 'admin/custom_change_list.html'
    advanced_search_fields = {}

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
        advanced_search_form = self.advanced_search_form(request.GET)
        extra_context = {'asf': advanced_search_form}

        if advanced_search_form is not None:
            request.GET._mutable = True

            for key in advanced_search_form.fields.keys():
                temp = request.GET.pop(key, None)
                if temp:  # there is a field but it's empty so it's useless
                    self.advanced_search_fields[key] = temp

            request.GET_mutable = False

        return super().changelist_view(request, extra_context=extra_context)

    def advanced_search(self, request, qs):
        qs = qs.filter(self.advanced_search_query(request, Q(), self.advanced_search_fields))
        self.advanced_search_fields = {}  # Clear CACHED Get values
        return qs

    def advanced_search_form(self, request=None):
        if hasattr(self, 'search_form'):
            return self.search_form(data=request)

        return None

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
