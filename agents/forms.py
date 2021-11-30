from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField

User = get_user_model()


class AgentModelForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email","phone","first_name","last_name","department",)
        field_classes = {'username': UsernameField}
    def clean_email(self):
        '''
        Verify email is available.
        '''
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email
    def clean_phone(self):
        '''
        Phone is available.
        '''
        phone = self.cleaned_data.get('phone')
        qs = User.objects.filter(phone=phone)
        if qs.exists():
            raise forms.ValidationError("phone number already in use")
        return phone