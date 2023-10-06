from django.urls import path,include
from coolingapp import views
from django.contrib.auth import views as auth_views
from coolingapp.views import (
    CustomPasswordChangeView,
    CustomPasswordChangeDoneView,
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView,
)
from django.conf import settings
from django.conf.urls.static import static

app_name = 'coolingapp'

urlpatterns = [
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"), name='password_reset_complete'),
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_change_done/', CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
    path('', view=views.index, name="index"),
    path("about", view=views.about, name="about"),
    path("dashboard/", view=views.dashboard, name="dashboard"),
    path("workpermit", view=views.workpermit, name="workpermit"),
    path("test", view=views.test, name="test"),
    path('maintenance', view=views.maintenance, name="maintenance"),
    path("account/register", view=views.register, name="register"),
    path("account/profile", view=views.profile, name="profile"),
    path("registration/login/", view=views.login_view, name="login"),
    path("logout", view=views.logout_view, name="logout"),
    path("activation/register_thankyou", view=views.register_thankyou, name="register_thankyou"),
    path("activation/activate/<str:uidb64>/<str:token>", view=views.activate, name="activate"),
    path('cooling_forecast/', views.cooling_forecast, name='cooling_forecast'),
    path("calendar", view=views.calendar, name="calendar"),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)