# -*- coding: utf-8 -*-
from django.db.models import (BooleanField, CharField, DateField, Model,
                              TextField)


class Area(Model):
    name = CharField(max_length=100)
    active = BooleanField(default=True)
    description = TextField(max_length=500)
    date = DateField()

    def __str__(self):
        return '{name}'.format(name=self.name)

    class Meta:
        verbose_name = 'Area'
        verbose_name_plural = 'Areas'
