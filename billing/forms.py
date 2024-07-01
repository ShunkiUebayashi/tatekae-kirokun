from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm as AuthPasswordChangeForm
from django.contrib.auth.forms import SetPasswordForm, UserCreationForm

from .models import PendingInvoice

User = get_user_model()


class PendingInvoiceForm(forms.ModelForm):
    receiver = forms.ModelChoiceField(queryset=User.objects.all())

    class Meta:
        model = PendingInvoice
        fields = ["receiver", "amount", "description"]
        widgets = {
            "amount": forms.NumberInput(attrs={"step": "0.01"}),
        }


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    secret_question = forms.CharField(max_length=255)
    secret_answer = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "secret_question", "secret_answer"]


class UsernameForm(forms.Form):
    username = forms.CharField(max_length=150)


class SecretAnswerForm(forms.Form):
    secret_answer = forms.CharField(max_length=255)
    new_password = forms.CharField(widget=forms.PasswordInput())


class CustomPasswordChangeForm(AuthPasswordChangeForm):
    class Meta:
        model = User
        fields = ["old_password", "new_password1", "new_password2"]
