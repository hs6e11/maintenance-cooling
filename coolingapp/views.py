from django.core.mail import send_mail,EmailMessage
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView,  PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from coolingapp.forms import RegisterForm, UserProfileForm, ExtendedProfileForm, ProfilePictureForm, CoolingForecastForm
from coolingapp.models import CustomUser, Profile, CoolingForecast
from django.views.generic.base import TemplateView

from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from coolingapp.utils.activation_token_generator import activation_token_generator
from django.contrib import messages

class CustomPasswordChangeDoneView(TemplateView):
    template_name = 'registration/password_change_done.html'

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'registration/password_change.html'  # Specify your template
    success_url = reverse_lazy('coolingapp:password_change_done')

    def form_valid(self, form):  
            response = super().form_valid(form)
            return response

#resetpassword

class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset.html'
    success_url = reverse_lazy('coolingapp:password_reset_done')
    
class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'
    
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('coolingapp:password_reset_complete')
    
class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'

# Create your views here.
def index(request):
    return render(request,"index.html")

@login_required
def about(request):
    return render(request,"about.html")

@login_required
def dashboard(request):
    forecasts = CoolingForecast.objects.all()
    context = {
        'forecasts': forecasts
    }
    return render(request, "dashboard.html", context)


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


def register(request: HttpRequest):
    # POST
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            #Register User
            user: CustomUser = form.save(commit=False)
            user.is_active = False
            user.save()

            # login(request, user)

            #Build email body HTML
            context = {
                "protocol": request.scheme,
                "host": request.get_host(),
                "uidb64": urlsafe_base64_encode(force_bytes(user.id)),
                "token": activation_token_generator.make_token(user)
            }
            email_body = render_to_string("activation/activate_email.html", context)

            #Sent email
            email = EmailMessage(
                to=[user.email],
                subject="Activate account",
                body=email_body
            )

            email.send()

            #Redirect to thank you
            return HttpResponseRedirect(reverse("coolingapp:register_thankyou"))
    else:
        form = RegisterForm()

    context = {"form": form}
    return render(request, "account/register.html", context)


def register_thankyou(request: HttpRequest):
    return render(request,"activation/register_thankyou.html")


def activate(request: HttpRequest, uidb64: str, token: str ):
    title = "Activate account successfully"
    description = "You can now log in !"

    #Decode user id
    id = urlsafe_base64_decode(uidb64).decode()

    try:
        user: CustomUser = CustomUser.objects.get(id=id)
        if not activation_token_generator.check_token(user, token):
            raise Exception("Check token false")
        user.is_active = True
        user.save()
    except:
        print("Activate doesn't pass.")
        title = "You can't activate your account"
        description = "This link has expired or has already been activated"

    context = {"title": title, "description": description}
    return render(request,"activation/activate.html", context)



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


def password_reset_confirmation(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        # Render the HTML email template with dynamic data
        html_message = render_to_string('registration/password_reset_email.html', {
            'username': user.username,
            'protocol': settings.WEB_PROTOCAL,
            'domain': settings.WEB_DOMAIN_NAME,
            'uid': uidb64,
            'token': token,
        })

        # Send the email
        send_mail(
            'Password Reset Confirmation',  # Subject
            'This is a plain text message. Your email client may not support HTML.',  # This will be ignored for HTML emails
            'from@example.com',
            [user.email],  # Recipient's email address
            fail_silently=False,
            html_message=html_message,  # HTML content
            content_subtype='html',  # Specify that it's HTML content
        )

        # Optionally, you can return an HttpResponse or redirect to a confirmation page
        return HttpResponse("Password reset confirmation email sent.")
    else:
        # Handle the case where the user is None or the token is invalid/expired
        # You can render an error page or redirect to an error view
        return HttpResponse("Invalid or expired reset link. Please try again.")

@login_required
def cooling_forecast(request: HttpRequest):
    if request.method == 'POST':
        form = CoolingForecastForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Forecast data saved successfully!")
            return HttpResponseRedirect(reverse("coolingapp:dashboard"))
    else:
        form = CoolingForecastForm()

    # Retrieve all saved CoolingForecast objects
    forecasts = CoolingForecast.objects.all()

    context = {
        'form': form,
        'forecasts': forecasts
    }
    return render(request, 'cooling_forecast.html', context)