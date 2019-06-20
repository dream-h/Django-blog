
from django import forms
from .base import BaseForm
from django.core.exceptions import ValidationError
from django.forms import fields, widgets


class LoginForm(BaseForm, forms.Form):
    """
    登录表单
    """
    username = fields.CharField(
        max_length=8,
        required=True,
        error_messages={
            'required': '用户名不能为空',
            'invalid': '用户名格式不对',
        }
    )

    # password = django_fields.RegexField(
    #     '^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$\%\^\&\*\(\)])[0-9a-zA-Z!@#$\%\^\&\*\(\)]{8,32}$',
    #     min_length=12,
    #     max_length=32,
    #     error_messages={'required': '密码不能为空.',
    #                     'invalid': '密码必须包含数字，字母、特殊字符',
    #                     'min_length': "密码长度不能小于8个字符",
    #                     'max_length': "密码长度不能大于32个字符"}
    # )

    password = fields.CharField()
    remb = fields.IntegerField(required=False)

    def clean_check_code(self):
        if self.request.session.get('CheckCode').upper() != self.request.POST.get('check_code').upper():
            raise ValidationError(message='验证码错误', code='invalid')


class RegisterForm(forms.Form):
    """
    用户注册表单
    """
    username = fields.CharField()
    nickname = fields.CharField()
    email = fields.EmailField()
    password = fields.CharField()
    confirm_pwd = fields.CharField()

    def clean_check_code(self):
        if self.request.session.get('CheckCode').upper() != self.request.POST.get('check_code').upper():
            raise ValidationError(message='验证码错误', code='invalid')

    def clean(self):
        pd1 = self.cleaned_data.get('password')
        pd2 = self.cleaned_data.get('confirm_pwd')
        if pd1 == pd2:
            pass
        else:
            raise ValidationError('密码输入不一致')

