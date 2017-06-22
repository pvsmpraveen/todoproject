from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'password'}))

class MyRegistrationForm(UserCreationForm):
    email = forms.EmailField(required = True)
    first_name = forms.CharField(required = False)
    last_name = forms.CharField(required = False)
    birthday = forms.DateField(required = False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self,commit = True):
        user = super(MyRegistrationForm, self).save(commit = False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.birthday = self.cleaned_data['birthday']

        if commit:
            user.save()

        return user