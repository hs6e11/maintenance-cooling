from django.contrib.auth.forms import UserCreationForm
from coolingapp.models import CustomUser, Profile, CoolingForecast, Event
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
        fields = UserCreationForm.Meta.fields + ("email", )

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
        fields = ("agency", "phone", "job_positions", "employee_id")

        widgets = {
            "agency": forms.TextInput(attrs={"placeholder": "Enter your agency"}),
            "phone": forms.TextInput(attrs={"placeholder": "Enter your phone number"}),
            "job_positions": forms.TextInput(attrs={"placeholder": "Enter your job positions"}),
            "employee_id": forms.TextInput(attrs={"placeholder": "Enter your employee_id"}),
        }

class ProfilePictureForm(forms.ModelForm):
    profile_picture = forms.ImageField(label="Profile Picture")
    class Meta:
        model = Profile
        fields = ("profile_picture", )

class CoolingForecastForm(forms.ModelForm):
    class Meta:
        model = CoolingForecast
        fields = [
            'InletTemp', 'OutletTemp', 'OutdoorWetBulb', 'OutdoorAirTemp', 
            'OutdoorAirHumidity', 'Kw_cooling', 'Kw_Chiller'
        ]
        widgets = {
            'InletTemp': forms.NumberInput(attrs={'placeholder': 'Enter Inlet Temperature', 'class': 'cooling-input'}),
            'OutletTemp': forms.NumberInput(attrs={'placeholder': 'Enter Outlet Temperature', 'class': 'cooling-input'}),
            'OutdoorWetBulb': forms.NumberInput(attrs={'placeholder': 'Enter Outdoor Wet Bulb', 'class': 'cooling-input'}),
            'OutdoorAirTemp': forms.NumberInput(attrs={'placeholder': 'Enter Outdoor Air Temperature', 'class': 'cooling-input'}),
            'OutdoorAirHumidity': forms.NumberInput(attrs={'placeholder': 'Enter Outdoor Air Humidity', 'class': 'cooling-input'}),
            'Kw_cooling': forms.NumberInput(attrs={'placeholder': 'Enter Kw Cooling', 'class': 'cooling-input'}),
            'Kw_Chiller': forms.NumberInput(attrs={'placeholder': 'Enter Kw Chiller', 'class': 'cooling-input'}),
        }

class EventForm(forms.ModelForm):
    
    title = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Title'})
    )
    
    description = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Description'}),
        required=False
    )
    
    start_time = forms.DateTimeField(
    widget=forms.TextInput(attrs={'class': 'datetimepicker', 'placeholder': 'Select start time', 'type': 'text'}),
    )

    end_time = forms.DateTimeField(
        widget=forms.TextInput(attrs={'class': 'datetimepicker', 'placeholder': 'Select end time', 'type': 'text'}),
        required=False
    )
    
    class Meta:
        model = Event
        fields = ['title', 'description', 'start_time', 'end_time']