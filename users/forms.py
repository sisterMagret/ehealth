from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import Patient, Agent, Category, FollowUp

User = get_user_model()


class PatientModelForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = "__all__"

    def clean_first_name(self):
        data = self.cleaned_data["first_name"]
        return data

    def clean(self):
        pass
        

class CustomUserCreationForm(UserCreationForm):
     class Meta:
        model = User
        fields = ("email","phone","first_name","last_name",)
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
        Verify email is available.
        '''
        phone = self.cleaned_data.get('phone')
        qs = User.objects.filter(phone=phone)
        if qs.exists():
            raise forms.ValidationError("phone number already in use")
        return phone

class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.none())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        agents = Agent.objects.filter(organisation=request.user.userprofile)
        super(AssignAgentForm, self).__init__(*args, **kwargs)
        self.fields["agent"].queryset = agents


class PatientCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = (
            'category',
        )


class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = (
            'name',
        )


class FollowUpModelForm(forms.ModelForm):
    class Meta:
        model = FollowUp
        fields = (
            'notes',
            'file'
        )











# from django import forms
# from django.contrib.auth import get_user_model
# from django.contrib.auth.forms import UserCreationForm, UsernameField
# from .models import Patient, Agent, Appointment

# User = get_user_model()


# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ("email","phone","first_name","last_name",)
#         field_classes = {'username': UsernameField}
#     def clean_email(self):
#         '''
#         Verify email is available.
#         '''
#         email = self.cleaned_data.get('email')
#         qs = User.objects.filter(email=email)
#         if qs.exists():
#             raise forms.ValidationError("email is taken")
#         return email
#     def clean_phone(self):
#         '''
#         Verify email is available.
#         '''
#         phone = self.cleaned_data.get('phone')
#         qs = User.objects.filter(phone=phone)
#         if qs.exists():
#             raise forms.ValidationError("phone number already in use")
#         return phone


# class AdminSigupForm(forms.ModelForm):
#     class Meta:
#         model=User
#         fields=['first_name','last_name','email','phone','password']
#         widgets = {
#         'password': forms.PasswordInput()
#         }


# class StaffUserForm(forms.ModelForm):
#     class Meta:
#         model=User
#         fields=['first_name','last_name','email','phone','password']
#         widgets = {
#         'password': forms.PasswordInput()
#         }
        
# class AgentForm(forms.ModelForm):
#     class Meta:
#         model=Agent
#         fields = "__all__"
#         # fields=['address','department','status','profile_pic']


# class PatientModelForm(forms.ModelForm):
#     assignedDoctorId=forms.ModelChoiceField(queryset=Agent.objects.all().filter(status=True),empty_label="Name and Department", to_field_name="user_id")
#     class Meta:
#         model = Patient
#         fields = "__all__"

#     # def clean_first_name(self):
#     #     data = self.cleaned_data["first_name"]
#     #     # if data != "Baldur":
#     #     #     raise ValidationError("Your name is not Joe")
#     #     return data

#     # def clean(self):
#     #     pass
#     #     # first_name = self.cleaned_data["first_name"]
#     #     # last_name = self.cleaned_data["last_name"]
#     #     # if first_name + last_name != "Joe Soap":
#     #     #     raise ValidationError("Your name is not Joe Soap")


# # class PatientForm(forms.Form):
# #     first_name = forms.CharField()
# #     last_name = forms.CharField()
# #     age = forms.IntegerField(min_value=0)


# class AssignAgentForm(forms.Form):
#     doctorId=forms.ModelChoiceField(queryset=Agent.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
#     patientId=forms.ModelChoiceField(queryset=Patient.objects.all().filter(status=True),empty_label="Patient Name and Symptoms", to_field_name="user_id")
#     class Meta:
#         model=Appointment
#         fields=['description','status']


# class PatientAppointmentForm(forms.ModelForm):
#     doctorId=forms.ModelChoiceField(queryset=Agent.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
#     class Meta:
#         model=Appointment
#         fields=['description','status']


# # class AppointmentForm(forms.ModelForm):
# #     doctorId=forms.ModelChoiceField(queryset=Agent.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
# #     patientId=forms.ModelChoiceField(queryset=Patient.objects.all().filter(status=True),empty_label="Patient Name and Symptoms", to_field_name="user_id")
# #     class Meta:
# #         model=Appointment
# #         fields=['description','status']


# # class PatientCategoryUpdateForm(forms.ModelForm):
# #     class Meta:
# #         model = Patient
# #         fields = (
# #             'category',
# #         )



# # class CategoryModelForm(forms.ModelForm):
# #     class Meta:
# #         model = Category
# #         fields = (
# #             'name',
# #         )


# # class FollowUpModelForm(forms.ModelForm):
# #     class Meta:
# #         model = FollowUp
# #         fields = (
# #             'notes',
# #             'file'
# #         )