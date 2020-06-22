from django import forms
from django.forms import CharField, EmailField
from .models import *


class SignupForm(forms.ModelForm):
    first_name = CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'minlength': 2,
                                                         'maxlength': 30,
                                                         'placeholder': 'First name'}))
    last_name = CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                        'minlength': 2,
                                                        'maxlength': 30,
                                                        'placeholder': 'Last name'}))
    username = CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                       'minlength': 5,
                                                       'maxlength': 30,
                                                       'placeholder': 'Username'}))
    nickname = CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                       'minlength': 5,
                                                       'maxlength': 30,
                                                       'placeholder': 'Nickname'}))

    avatar_path = forms.ImageField(
        widget=forms.ClearableFileInput(),
        required=False, label=u'Avatar'
    )

    email = EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}))
    password = CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                           'placeholder': 'Password'}))
    password_confirmation = CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                        'placeholder': 'Password confirmation'}))

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'username', 'email', 'avatar_path',)


class UserSettingsForm(forms.ModelForm):
    first_name = CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'minlength': 2, 'maxlength': 30, }))
    last_name = CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'minlength': 2, 'maxlength': 30, }))

    username = CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'minlength': 5, 'maxlength': 30, }))
    nickname = CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'minlength': 5, 'maxlength': 30, }))

    email = EmailField(required=False,
                       widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}))
    avatar_path = forms.ImageField(
        widget=forms.ClearableFileInput(),
        required=False, label=u'Avatar'
    )

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'username', 'email',)


class AskForm(forms.ModelForm):
    title = CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                    'maxlength': 100,
                                                    'minlength': 10,
                                                    'placeholder': 'Add title'}))

    text = CharField(widget=forms.Textarea(attrs={'class': 'form-control',
                                                  'minlength': 30,
                                                  'placeholder': 'Describe your question in details'}))

    tags = CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'maxlength': 40,
                                                   'placeholder': 'Enter tags separated with a '
                                                                  'space'}))

    class Meta:
        model = Question
        fields = ('title', 'text', 'tags',)


class AnswerForm(forms.ModelForm):
    text = CharField(widget=forms.Textarea(attrs={'class': 'form-control',
                                                  'minlength': 20,
                                                  'placeholder': 'Enter your reply text'}))

    class Meta:
        model = Answer
        fields = ('text',)


class SettingsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('username', 'email', 'nickname', 'avatar_path',)


class LoginForm(forms.ModelForm):
    username = CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                       'maxlength': 30,
                                                       'placeholder': 'Enter username'}))

    password = CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                           'placeholder': 'Enter password'}))

    class Meta:
        model = Profile
        fields = ('username', 'password',)
