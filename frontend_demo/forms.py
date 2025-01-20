from typing import Any
from django import forms
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


User = get_user_model()


class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Enter your comment', 'style': 'width:100%', 'class': 'form-control',
               'data-rule': 'required', 'data-msg': 'Please write your comment'}
    ))


class CreateUserForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'Enter your email...', 'class': 'form-control'}
    ))
    password = forms.CharField(max_length=30, widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter your password...', 'class': 'form-control'}
    ))
    confirm_password = forms.CharField(max_length=30, widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter your confirm password...',
               'class': 'form-control'}
    ))

    def clean(self) -> dict[str, Any]:

        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']

        # Validate password confirmation and add error to confirm_password field
        if password != confirm_password:
            self.add_error('confirm_password',
                           'Password and Confirm password do not match')

        # Validate password strength and add error to password field
        try:
            validate_password(password)
        except ValidationError as e:
            self.add_error('password', str(e))

        # Check if the email already exists in the database and add error to email field
        if User.objects.filter(email=email).exists():
            self.add_error('email', 'Email already exists')

        return super().clean()
