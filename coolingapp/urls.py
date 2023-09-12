from django.urls import path,include
from coolingapp import views

app_name = 'coolingapp'
urlpatterns = [

    path('',views.index, name="index"),
    path('about',views.about, name="about"),
    path('dashboard',views.dashboard, name="dashboard"),
    path('workpermit',views.workpermit, name="workpermit"),
    path('test',views.test, name="test"),
    path('maintenance',views.maintenance, name="maintenance"),
    path("account/register",views.register, name="register"),
    path("registration/login/",views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),

]