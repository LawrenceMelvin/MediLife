from django import forms
from .models import *
import re
from django.contrib import messages


class DoctorRegisterForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'phone', 'email', 'location', 'gender', 'password']
        widgets = {
            'name': forms.TextInput(
                attrs={'cols': 80, 'rows': 20, 'placeholder': 'User name', 'class': 'form-login',
                       'style': 'color:#000b46'}),
            'phone': forms.TextInput(attrs={'cols': 80, 'rows': 20, 'placeholder': 'Phone', 'class': 'form-login',
                                            'style': 'color:#000b46'}),
            'email': forms.TextInput(
                attrs={'cols': 80, 'rows': 20, 'placeholder': 'Email Id', 'class': 'form-login',
                       'style': 'color:#000b46'}),
            'gender': forms.TextInput(attrs={'cols': 80, 'rows': 20, 'placeholder': 'Phone', 'class': 'form-login',
                                             'style': 'color:#000b46'}),
            'location': forms.TextInput(
                attrs={'cols': 80, 'rows': 20, 'placeholder': 'Address', 'class': 'form-login',
                       'style': 'color:#000b46'}),
            'password': forms.PasswordInput(
                attrs={'cols': 80, 'rows': 20, 'placeholder': 'Password', 'class': 'form-login',
                       'style': 'color:#000b46'}),

        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', password):
            raise forms.ValidationError("password must contains(caps and small letter)")
        return password

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.fullmatch(r'[6789][0-9]{9,}', phone):
            raise forms.ValidationError("Enter a valid phone number")
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
            raise forms.ValidationError("Enter a valid phone number")
        return email



class PatientRegisterForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'phone', 'email', 'location', 'gender', 'password']
        widgets = {
            'name': forms.TextInput(
                attrs={'cols': 80, 'rows': 20, 'placeholder': 'User name', 'class': 'form-login',
                       'style': 'color:#000b46'}),
            'phone': forms.TextInput(attrs={'cols': 80, 'rows': 20, 'placeholder': 'Phone', 'class': 'form-login',
                                            'style': 'color:#000b46'}),
            'email': forms.TextInput(
                attrs={'cols': 80, 'rows': 20, 'placeholder': 'Email Id', 'class': 'form-login',
                       'style': 'color:#000b46'}),
            'gender': forms.TextInput(attrs={'cols': 80, 'rows': 20, 'placeholder': 'Phone', 'class': 'form-login',
                                             'style': 'color:#000b46'}),
            'location': forms.TextInput(
                attrs={'cols': 80, 'rows': 20, 'placeholder': 'Address', 'class': 'form-login',
                       'style': 'color:#000b46'}),
            'password': forms.PasswordInput(
                attrs={'cols': 80, 'rows': 20, 'placeholder': 'Password', 'class': 'form-login',
                       'style': 'color:#000b46'}),

        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', password):
            raise forms.ValidationError("password must contains(caps and small letter)")
        return password

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.fullmatch(r'[6789][0-9]{9,}', phone):
            raise forms.ValidationError("Enter a valid phone number")
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
            raise forms.ValidationError("Enter a valid phone number")
        return email

