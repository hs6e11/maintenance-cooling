from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from coolingapp.forms import RegisterForm, UserProfileForm, ExtendedProfileForm, ProfilePictureForm
from coolingapp.models import CustomUser, Profile
from django.views.generic.base import TemplateView

class CustomPasswordChangeDoneView(TemplateView):
    template_name = 'registration/password_change_done.html'

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'registration/password_change.html'  # Specify your template
    success_url = reverse_lazy('coolingapp:password_change_done')

    def form_valid(self, form):  
            response = super().form_valid(form)
            return response

# Create your views here.
def index(request):
    return render(request,"index.html")

@login_required
def about(request):
    return render(request,"about.html")

@login_required
def dashboard(request):
    return render(request,"dashboard.html")

@login_required
def workpermit(request):
    return render(request,"workpermit.html")

@login_required
def test(request):
    return render(request,"test.html")

@login_required
def maintenance(request):
    return render(request,"maintenance.html")

def logout_view(request):
    logout(request)
    return render(request,'index.html')


def login_view(request):
    # Check if the user is already authenticated
    if request.user.is_authenticated:
        return render(request, 'index.html')  # Redirect to the home page or another appropriate page

    # If the request method is POST, the user submitted the login form
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Authenticate the user
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Log in the user
                login(request, user)
                return render(request, 'index.html')  # Redirect to the home page or another appropriate page after successful login
    else:
        form = AuthenticationForm()

    # Render the login page with the login form
    return render(request, 'registration/login.html', {'form': form})


def register(request):
    # POST
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return render(request, 'index.html')
    else:
        form = RegisterForm()

    context = {"form": form}
    return render(request, "account/register.html", context)

def logout_view(request):
    logout(request)
    return render(request,'index.html')

@login_required
def profile(request: HttpRequest):
    user = request.user
    #POST
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        is_new_profile = False
       
        try:
            #Will update
            extended_form = ExtendedProfileForm(request.POST, instance=user.profile)
            profile_picture_form = ProfilePictureForm(request.POST, request.FILES, instance=user.profile)
        except:
            #Will create
            extended_form = ExtendedProfileForm(request.POST)
            profile_picture_form = ProfilePictureForm(request.POST)
            is_new_profile = True

        if form.is_valid() and extended_form.is_valid() and profile_picture_form.is_valid():
            form.save()
            if is_new_profile:
                # Create
                profile = extended_form.save(commit=False)
                profile.user = user  # Assign the user to the profile
                profile.save()
                profile_picture_form.instance = profile  # Assign the profile to the profile picture form's instance
                profile_picture_form.save()
            else:
                # Update
                extended_form.save()
                profile_picture_form.save()

            return HttpResponseRedirect(reverse("coolingapp:profile"))
    
    else:
        form = UserProfileForm(instance=user)
        try:
            extended_form = ExtendedProfileForm(instance=user.profile)
            profile_picture_form = ProfilePictureForm(instance=user.profile)
        except:
            extended_form =  ExtendedProfileForm()
            profile_picture_form = ProfilePictureForm()

    #GET
    context = {
        "form": form,
        "extended_form": extended_form,
        "profile_picture_form": profile_picture_form,
    }
    return render(request, "account/profile.html", context)