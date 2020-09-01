from django.shortcuts import render
from .models import Ketab
from .forms import KetabForm
from django.views.generic import CreateView, DeleteView,ListView,DetailView, UpdateView
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


from django.shortcuts import redirect

def redirect_view(request):
    response = redirect('/ketab')
    return response

class KetabCreateView(LoginRequiredMixin, CreateView):
    template_name = "ketab/ketab_create.html"
    form_class = KetabForm


class KetabDetailView(DetailView):
    model = Ketab
    template_name = "ketab/ketab_detail.html"


    # override context data
    def get_context_data(self, *args, **kwargs):
        context = super(KetabDetailView,
                        self).get_context_data(*args, **kwargs)
        # add extra field
        context["page_landing_title"] = "Detail View"
        return context


class KetabUpdateView(LoginRequiredMixin, UpdateView):
    model = Ketab
    template_name = "ketab/ketab_create.html"

    fields= ['title', 'content', 'image',
             'created_date', 'publish_date', 'draft', 'tags']

    success_url = reverse_lazy('ketab_list')


class KetabListView(ListView):
    paginate_by = 4
    model = Ketab
    template_name = "ketab/ketab_list.html"



class KetabDeleteView(LoginRequiredMixin, DeleteView):
    model = Ketab
    template_name = "ketab/ketab_delete.html"
    success_url = reverse_lazy('ketab_list')
