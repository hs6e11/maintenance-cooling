from django.contrib.auth.forms import UserCreationForm
from coolingapp.models import CustomUser, Profile  # Import Profile model
from django import forms

class RegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder": "Email"}))
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Please enter username with employee ID"})
    )
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}),
        strip=False,
    )
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ("email",)

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, help_text="Required. 30 characters or fewer.", widget=forms.TextInput(attrs={"placeholder": "First Name"}))
    last_name = forms.CharField(max_length=30, required=True, help_text="Required. 30 characters or fewer.", widget=forms.TextInput(attrs={"placeholder": "Last Name"}))
    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name")

class ExtendedProfileForm(forms.ModelForm):
    prefix = "extended"

    class Meta:
        model = Profile
        fields = ("address", "phone", "job_positions", "profile_picture")

        widgets = {
            "address": forms.Textarea(attrs={"rows": 3, "placeholder": "Enter your address"}),
            "phone": forms.TextInput(attrs={"placeholder": "Enter your phone number"}),
            "job_positions": forms.TextInput(attrs={"placeholder": "Enter your job positions"}),
        }
