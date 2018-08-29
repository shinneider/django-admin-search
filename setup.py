# -*- coding: utf-8 -*-
#!/usr/bin/env python
from io import open
from setuptools import find_packages, setup
from django_admin_search.meta import VERSION


setup(
    name='django-admin-search',
    version=str(VERSION),
    description='The "Django Admin Search" is a advanced search modal for django admin',
    long_description=open('README.md', encoding='utf-8').read(),
    author='Shinneider Libanio da Silva',
    author_email='shinneider-libanio@hotmail.com',
    url='https://github.com/shinneider/django_admin_search',
    license='MIT',
    packages=find_packages() + [
        'django_admin_search/templates', 
        'django_admin_search/static',
        'django_admin_search/locale'
    ],
    install_requires=[
        # 'Django>=2.0',
        # 'Python>=3.5',
    ],
    include_package_data=True,
)