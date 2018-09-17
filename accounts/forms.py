from django import forms
from accounts.models import User
import hashlib
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse


def hash_code(s, salt='confirm'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


class LoginForm(forms.Form):
    email = forms.CharField(label="", max_length=128,required=True,
                               widget=forms.TextInput(attrs={'id':'email', 'class': 'form-control input-medium','placeholder':'用户名或邮箱'}))
    password = forms.CharField(label="", max_length=256,
                               widget=forms.PasswordInput(attrs={'id':'password', 'class': 'form-control input-medium','placeholder':'密码'}))

    def clean(self):
        accounts = self.cleaned_data['email']
        password = self.cleaned_data['password']
        password = hash_code(password)
        if User.objects.filter(email=accounts):
            user = User.objects.get(email=accounts)
        else:
            if User.objects.filter(username=accounts):
                user = User.objects.get(username=accounts)
            else:
                message = '无效账户'
                self.cleaned_data['message'] = message
                return self.cleaned_data
            if not user.password == password:
                message = '密码错误'
                self.cleaned_data['message'] = message
                return self.cleaned_data
            else:
                self.cleaned_data['user'] = user
                message = 'Login successful'
                self.cleaned_data['message'] = message
                return self.cleaned_data


class RegisterForm(forms.Form):
    username = forms.CharField(label='', max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '用户名'}
    ))
    password1 = forms.CharField(label='', max_length=256, widget=forms.PasswordInput(
        attrs={'class':'form-control', 'placeholder':'密码（别挑战你的记忆力了）'}
    ))
    password2 = forms.CharField(label='', max_length=256, widget=forms.PasswordInput(
        attrs={'class':'form-control', 'placeholder':'请重复密码'}
    ))
    email = forms.EmailField(label='', widget=forms.EmailInput(
        attrs={'class':'form-control', 'placeholder':'邮箱'}
    ))


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = {'username', 'email'}
        labels = {'username':'username', 'email':'email'}
        widgets = {'username': forms.TextInput(attrs={'class': 'form-control'}),
                   'email': forms.EmailInput(attrs={'class': 'form-control'})}


class PswForm(forms.Form):
    password1 = forms.CharField(label='New Password', max_length=256, widget=forms.PasswordInput(
        attrs={'class': 'form-control'}
    ))
    password2 = forms.CharField(label='Confirmation password', max_length=256, widget=forms.PasswordInput(
        attrs={'class': 'form-control'}
    ))