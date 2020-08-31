from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin



# Register out own model admin, based on the default UserAdmin
@admin.register(Account)
class KetabModelAdmin(admin.ModelAdmin):


    class Meta:
        model = Account

