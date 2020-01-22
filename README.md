Django Admin Search
===================

The "Django Admin Search" is a advanced search modal for django admin.

If you use or like the project, click `Star` and `Watch` to generate metrics and i evaluate project continuity.

# Install:
    pip install django-admin-search

# Usage:

1. Add to your INSTALLED_APPS, in settings.py:
    ```
    INSTALLED_APPS = [  
        ...
        'django_admin_search',
        ...
    ]
    ```

2. Create a search form for model:
    ```
    from .models import Area
    from django.forms import ModelForm, Form
    from django.forms import DateField, CharField, ChoiceField, TextInput


    class YourFormSearch(Form):
        name = CharField(required=False)
        date = DateField(required=False, widget=TextInput(
            attrs={ 
                'filter_method': '__gte',
            }
        ))
    ```

3. In your admin:
    ```
    from django_admin_search.admin import AdvancedSearchAdmin
    from .models import YourModel
    from .form import YourForm, YourFormSearch

    @register(YourModel)
    class YourAdmin(AdvancedSearchAdmin):
        form = YourForm
        search_form = YourFormSearch
    ```

# Advanced:
1. to multiple filters in same field:
    ```
    class YourFormSearch(Form):
        ...
        name = CharField(required=False)
        begin = DateField(required=False, widget=TextInput(
            attrs={
                'filter_field': 'date', 
                'filter_method': '__gte',
            }
        ))
        end = DateField(required=False, widget=TextInput(
            attrs={
                'filter_field': 'date', 
                'filter_method': '__lte',
            }
        ))
    ```

2. add placeholder and mask
    ```
    class YourFormSearch(Form):
        ...
        date = DateField(required=False, widget=TextInput(
            attrs={
                'data-mask': "00/00/0000", 
                'placeholder': 'MM/DD/YYYY'
            }
        ))
    ```

3. Custom filter query for a field
    ```
    from django_admin_search.admin import AdvancedSearchAdmin
    from .models import YourModel
    from .form import YourForm, YourFormSearch

    @register(YourModel)
    class YourAdmin(AdvancedSearchAdmin):
        def search_FieldNameHere(request, field_value, param_values):
            """
                intercept query filter for description field
            """
            query = Q()
            # your Q logic here
            return query
    ```

# Images:

Button in admin list:
    ![input](https://user-images.githubusercontent.com/30196992/59556917-19182f00-8fa2-11e9-9d9a-955d73d79d11.png)

Modal opened:
    ![modal](https://user-images.githubusercontent.com/30196992/59556920-29c8a500-8fa2-11e9-8677-0f340762e64a.png)


# Development and Running the Tests
To do development work for Django Admin Search, clone it locally, make and activate a virtualenv for it, then from within the project directory:
```
pip install -e .[dev]
```

To run the tests:
```
pytest
```

If your work in high difficult test, and need to re run the test every time, use `pytest-watch`:
```
ptw  # this see file change and re run a test
```

when you need to see passed lines by test, run 
```
pytest --cov-report html
```
after this, will be created a `htmlcov` folder in the root 

See your code quality in Sonar (in testing, no metrics to approve yet)
```
https://sonarcloud.io/dashboard?id=shinneider_django-admin-search
```

For future i want to run test's in Travis CI, to check if PR is Ok, but to be effective, i need to cover 80% or more of the code, help-me creating a test case, see this issue [PR - 20](https://github.com/shinneider/django-admin-search/issues/20)
