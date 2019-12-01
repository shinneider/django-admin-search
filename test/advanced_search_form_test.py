from django.test import SimpleTestCase
from django.template import Context, Template
from django.template.loader import render_to_string

from django_admin_search.templatetags.advanced_search_form import advanced_search_form
from test.mocks import CLMock, TestSearchForm


class TestAdvancedSearchTemplateTag(SimpleTestCase):

    def test_templatag_render(self):
        form = TestSearchForm()
        context = Context({'cl': CLMock, 'asf': form})
        template = Template(
            '{% load advanced_search_form %}'
            '{% advanced_search_form cl %}'
        ).render(context)

        for field, _ in form.fields.items():
            # search fields in template
            self.assertIn(str(form[field]), template)
            # search fields label's in template
            self.assertIn(form[field].label_tag(), template)

    def test_templatag_render_without_asf(self):
        context = Context({'cl': CLMock})
        template = Template(
            '{% load advanced_search_form %}'
            '{% advanced_search_form cl %}'
        ).render(context)
        self.assertEqual('', template)