from django.contrib import admin
from django.urls import include, path
from django.utils import timezone
from django.contrib.auth import views as auth_views
from dashboard.background_task import *
from background_task.models import Task, CompletedTask
from account.views import (
    registration_view,
    login_view,
    logout_view
)
from dashboard.views import (
    home_view,
    getting_started_view,
    help_view,
)
"""
Tasks, when stored in database, are prepended with the app name.
This will clear tasks for the current app only.
"""
try:
    Task.objects.all().delete()
    CompletedTask.objects.all().delete()
except:
    pass

date = timezone.datetime.today()
midnight = date.replace(hour=00, minute=00, second=00)
# load_model(schedule=5)
# act(schedule=midnight, repeat=3600)  # repeat 1 hr
# save_pnl(schedule=midnight, repeat=86400)  # repeat 24 hrs

urlpatterns = [
    path('', home_view, name='home'),
    path('getting_started/', getting_started_view, name='getting_started'),
    path('help/', help_view, name='help'),
    path('register/', registration_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', include('dashboard.urls'), name='dashboard'),
    path('admin/', admin.site.urls),
    path("password_reset/", auth_views.PasswordResetView.as_view(template_name="account/password_reset.html"),
         name="password_reset"),
    path("password_reset/done/",
         auth_views.PasswordResetDoneView.as_view(template_name="account/password_reset_done.html"),
         name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>",
         auth_views.PasswordResetConfirmView.as_view(template_name="account/password_reset_confirm.html"),
         name="password_reset_confirm"),
    path("password-reset-complete/",
         auth_views.PasswordResetCompleteView.as_view(template_name="account/password_reset_complete.html"),
         name="password_reset_complete")
]
