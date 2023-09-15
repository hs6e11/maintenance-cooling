from django.urls import path,include
from coolingapp import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'coolingapp'
urlpatterns = [

    path('',view=views.index, name="index"),
    path('about',view=views.about, name="about"),
    path('dashboard',view=views.dashboard, name="dashboard"),
    path('workpermit',view=views.workpermit, name="workpermit"),
    path('test',view=views.test, name="test"),
    path('maintenance',view=views.maintenance, name="maintenance"),
    path("account/register",view=views.register, name="register"),
    path("account/profile",view=views.profile, name="profile"),
    path("registration/login/",view=views.login_view, name="login"),
    path("logout", view=views.logout_view, name="logout"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)