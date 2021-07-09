from django import forms


class UserForm(forms.Form):
    username = forms.CharField(
        label="用户名",
        max_length=128,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        label="密码",
        max_length=256,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegisterForm(forms.Form):
    gender = (
        ('secret', '保密'),
        ('male', '男'),
        ('female', '女'),
    )
    username = forms.CharField(
        label="用户名",
        max_length=128,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(
        label="密码（4-256位）",
        min_length=4,
        max_length=256,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(
        label="确认密码",
        min_length=4,
        max_length=256,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(
        label="邮箱地址（用于找回密码）",
        widget=forms.EmailInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='性别', choices=gender)


class FindbackForm(forms.Form):
    username = forms.CharField(
        label="用户名",
        max_length=128,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(
        label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(
        label="新密码",
        max_length=256,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(
        label="确认密码",
        max_length=256,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class AskForm(forms.Form):
    content = forms.CharField(label="问题内容（不超过128字）",
                              max_length=128,
                              widget=forms.TextInput(attrs={
                                  'class': 'form-control',
                              }))
    description = forms.CharField(
        label="问题描述（不超过1024字）",
        max_length=1024,
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control'}))


class AnswerForm(forms.Form):
    content = forms.CharField(
        label="您的回答（不超过1024字）",
        max_length=1024,
        widget=forms.Textarea(attrs={'class': 'form-control'}))
