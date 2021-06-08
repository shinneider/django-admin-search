# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.admin import ModelAdmin
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from django_admin_search import utils


class AdvancedSearchAdmin(ModelAdmin):
    """
        class to add custom filters in django admin
    """
    change_list_template = 'admin/custom_change_list.html'
    advanced_search_fields = {}
    search_form_data = None

    def get_queryset(self, request):
        """
            override django admin 'get_queryset'
        """
        queryset = super().get_queryset(request)
        try:
            return queryset.filter(self.advanced_search_query(request))
        except Exception:
            messages.add_message(request, messages.ERROR, 'Filter not applied, error has occurred')
            return queryset.none()

    def changelist_view(self, request, extra_context=None):
        self.advanced_search_fields = {}
        self.search_form_data = self.search_form(request.GET)
        self.extract_advanced_search_terms(request.GET)
        extra_context = {'asf': self.search_form_data}
        return super().changelist_view(request, extra_context=extra_context)

    def extract_advanced_search_terms(self, request):
        request._mutable = True  # pylint: disable=W0212

        if self.search_form_data is not None:
            for key in self.search_form_data.fields.keys():
                temp = request.pop(key, None)
                if temp:  # there is a field but it's empty so it's useless
                    self.advanced_search_fields[key] = temp

        request._mutable = False  # pylint: disable=W0212

    def get_field_value(self, field):
        """
            check if field has value passed on request
        """
        if field in self.advanced_search_fields:
            return True, self.advanced_search_fields[field][0]

        return False, None

    @staticmethod
    def get_field_value_default(field, form_field, field_value, has_field_value, request):
        """
            mount default field value
        """
        if has_field_value:
            field_name = form_field.widget.attrs.get('filter_field', field)
            field_filter = field_name + form_field.widget.attrs.get('filter_method', '')

            try:
                field_value = utils.format_data(form_field, field_value)  # format by field type
                return Q(**{field_filter: field_value})
            except ValidationError:
                messages.add_message(request, messages.ERROR, _(f"Filter in field `{field_name}` "
                                                                "ignored, because value "
                                                                f"`{field_value}` isn't valid"))
            except Exception:
                messages.add_message(request, messages.ERROR, _(f"Filter in field `{field_name}` "
                                                                "ignored, error has occurred."))

        return Q()

    def get_field_value(self, field, form_field, field_value, has_field_value, request):
        """
            allow to override default field query
        """
        if hasattr(self, ('search_' + field)):
            return getattr(self, 'search_' + field)(field, field_value, form_field, request,
                                                    self.advanced_search_fields)

        return self.get_field_value_default(field, form_field, field_value, has_field_value, request)

    def advanced_search_query(self, request):
        """
            Get form and mount filter query if form is not none
        """
        query = Q()

        if self.search_form_data is None:
            return query

        for field, form_field in self.search_form_data.fields.items():
            has_field_value, field_value = self.get_field_value(field)
            query &= self.get_field_value(field, form_field, field_value, has_field_value, request)

        return query
