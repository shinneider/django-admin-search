from django.contrib.admin.views.main import SEARCH_VAR
from django.template import Library

register = Library()


@register.inclusion_tag('admin/custom_search_form.html', takes_context=True)
def advanced_search_form(context, cl):
    """
    Displays a search form for searching the list.
    """
    return {
        'asf' : context.get('asf'),
        'cl': cl,
        'show_result_count': cl.result_count != cl.full_result_count,
        'search_var': SEARCH_VAR
    }