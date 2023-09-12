from django.contrib.auth.forms import UserCreationForm
from coolingapp.models import CustomUser, Profile
from django import forms


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name")


class ExtendedProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("address", "phone", "job_positions")