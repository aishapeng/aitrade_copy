from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account


class AccountAdmin(UserAdmin):
    # shows in list in admin panel
    list_display = ('email', 'username', 'date_joined', 'last_login')
    # create search bar
    search_fields = ('email', 'username')
    # will not be changed
    readonly_fields = ('date_joined', 'last_login')
    # exclude user's secret key
    exclude = ('secretKey',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)