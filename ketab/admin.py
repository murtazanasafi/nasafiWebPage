from django.contrib import admin
from .models import Ketab
# Register your models here.

@admin.register(Ketab)
class KetabModelAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'title', 'created_date', 'publish_date', 'tag_list']

    class Meta:
        model = Ketab

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self,obj):
        return u', '.join(o.name for o in obj.tags.all())


