# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.admin import ModelAdmin
from django.contrib.admin.views.main import ChangeList
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from django_admin_search import utils


class AdvancedSearchAdmin(ModelAdmin):
    """
        class to add custom filters in django admin
    """
    change_list_template = 'admin/custom_change_list.html'
    advanced_search_fields = {}

    def get_queryset(self, request):
        """
            override django admin 'get_queryset'
        """
        queryset = super().get_queryset(request)
        try:
            return queryset.filter(
                self.advanced_search_query(request)
            )
        except Exception as err:
            messages.add_message(request, messages.ERROR, str(err))
            return queryset.none()
        
    def changelist_view(self, request, extra_context=None):
        self.search_form_data = self.search_form(request.GET)
        self.extract_advanced_search_terms(request.GET)
        extra_context = {'asf': self.search_form_data}
        return super().changelist_view(request, extra_context=extra_context)

    def extract_advanced_search_terms(self, request):
        request._mutable = True

        if self.search_form_data is not None:
            for key in self.search_form_data.fields.keys():
                temp = request.pop(key, None)
                if temp:  # there is a field but it's empty so it's useless
                    self.advanced_search_fields[key] = temp

        request._mutable = False

    def advanced_search_query(self, request):
        """
            Get form and mount filter query if form is not none
        """
        query = Q()
        param_values = self.advanced_search_fields
        
        form = self.search_form_data
        if form is None:
            return query

        for field, form_field in self.search_form_data.fields.items():
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
                field_value = utils.format_data(form_field, field_value)  # format by field type
                query &= Q(**{field_filter: field_value})
            except ValidationError as err:
                messages.add_message(request, messages.ERROR, 
                    _("Filter in field `{field}` ignored, because value `{value}` isn't valid").format(
                        value=field_value, field=field_name
                    )
                )
                continue
            except Exception as err:
                messages.add_message(request, messages.ERROR, 
                    _("Filter in field `{field}` ignored, error has occurred.").format(
                        err=err, field=field_name
                    )
                )
                continue
        
        print(1111, query)
        return query
