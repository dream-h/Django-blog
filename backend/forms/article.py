from django import forms
from django.forms import fields, widgets
from repository import models


class ArticlePost(forms.Form):
    """
    文章表单
    """
    title = fields.CharField(
        widget=widgets.TextInput(
            attrs={"class": 'form-control', "placeholder": '请输入文章标题'}
        )
    )
    summary = fields.CharField(
        widget=widgets.Textarea(
            attrs={
                "class": 'form-control',
                "placeholder": '请输入文章简介',
                "rows": '3'
            }
        )
    )
    body = fields.CharField(
        widget=widgets.Textarea(
            attrs={"class": 'kind-content'}
        )
    )

    article_type_id = fields.IntegerField(
        widget=widgets.ChoiceWidget(choices=models.Article.type_choice)
    )
    category_id = fields.ChoiceField(
        choices=[],
        widget=widgets.RadioSelect
    )
    tags = fields.MultipleChoiceField(
        choices=[],
        widgets=widgets.CheckboxSelectMultiple
    )

    def __init__(self, request, *args, **kwargs):
        super(ArticlePost, self).__init__(*args, **kwargs)
        blog_id = request.session['user_info']['blog__nid']
        self.fields['category_id'].choices = \
            models.Category.objects.filter(blog=blog_id).values_list('nid', 'title')
        self.fields['tags'].choices = \
            models.Tag.objects.filter(blog=blog_id).values_list('nid', 'title')

