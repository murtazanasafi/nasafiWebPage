from django import forms, utils

from .models import Ketab

from pagedown.widgets import PagedownWidget

class KetabForm(forms.ModelForm):
    created_date = forms.DateField(widget=forms.SelectDateWidget, initial=utils.timezone.now())
    publish_date = forms.DateField(widget=forms.SelectDateWidget, initial=utils.timezone.now())
    content = forms.CharField(widget=PagedownWidget)

    class Meta:
        model = Ketab

        fields = [
                'title',
                'content',
                'image',
                'draft',
                'publish_date',
                'tags',
                  ]