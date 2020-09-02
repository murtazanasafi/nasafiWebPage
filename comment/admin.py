from django.contrib import admin
from .models import Comment
from django.contrib.auth.admin import UserAdmin


# Register your models here.
# Register out own model admin, based on the default UserAdmin
@admin.register(Comment)
class KetabModelAdmin(admin.ModelAdmin):


    class Meta:
        model = Comment

