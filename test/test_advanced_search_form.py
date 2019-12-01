from django_admin_search.templatetags.advanced_search_form import advanced_search_form

from django.test import SimpleTestCase
from django.template import Context, Template


class TestAdvancedSearchTemplateTag(SimpleTestCase):
    pass

    # def test_rendered(self):
    #     context = Context({'title': 'my_title'})
    #     template_to_render = Template(
    #         '{% load advanced_search_form %}'
    #         '{% advanced_search_form %}'
    #     )
    #     rendered_template = template_to_render.render(context)
    #     self.assertInHTML('<h1>my_title</h1>', rendered_template)