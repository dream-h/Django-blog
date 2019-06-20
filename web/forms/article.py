#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.core.exceptions import ValidationError
from django import forms as django_forms
from django.forms import fields as django_fields
from django.forms import widgets as django_widgets

from repository import models


class ArticleForm(django_forms.Form):
    title = django_fields.CharField(
        widget=django_widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '文章标题'})
    )
    summary = django_fields.CharField(
        widget=django_widgets.Textarea(attrs={'class': 'form-control', 'placeholder': '文章简介', 'rows': '3'})
    )
    body = django_fields.CharField(
        widget=django_widgets.Textarea(attrs={'class': 'kind-content'})
    )
    article_type_id = django_fields.IntegerField(
        widget=django_widgets.RadioSelect(choices=models.Article.type_choice)
    )
    category_id = django_fields.ChoiceField(
        choices=[],
        widget=django_widgets.RadioSelect
    )

    tags = django_fields.MultipleChoiceField(
        choices=[],
        widget=django_widgets.CheckboxSelectMultiple
    )

    def __init__(self, request, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        blog_id = request.session['user_info']['blog__nid']
        self.fields['category_id'].choices = models.Category.objects.filter(blog_id=blog_id).values_list('nid','title')
        self.fields['tags'].choices = models.Tag.objects.filter(blog_id=blog_id).values_list('nid', 'title')


'''
class ArticleForm(BaseForm, forms.Form):
    """
    文章表单
    """
    title = fields.CharField(
        widget=forms.TextInput(attrs={
            'name': "title",
            'class': "form-control",
            'placeholder': '请输入标题',
        })
    )
    summary = fields.CharField(
        widget=forms.TextInput(attrs={
            'name': "summary",
            'class': "form-control",
            'placeholder': '请输入简介',
        })
    )
    body = fields.CharField(
        widget=forms.widgets.Textarea(
            attrs={
                'name': "body",
                'class': "form-control",
            }
        ),
    )

    type_choice = [
        (1, 'Python'),
        (2, 'Django'),
        (3, 'book'),
        (4, '区块链'),
        (5, '人工智能'),
    ]
    article_type_id = fields.IntegerField(
            widget=forms.RadioSelect(
                choices=type_choice,

        )
    )

    tag = fields.CharField()
    category = fields.CharField()

'''

