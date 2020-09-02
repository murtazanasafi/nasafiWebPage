from django.shortcuts import render
from .models import Ketab
from .forms import KetabForm
from django.views.generic import CreateView, DeleteView,ListView,DetailView, UpdateView
from django.urls import reverse_lazy


from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger


from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


from django.shortcuts import redirect

def redirect_view(request):
    response = redirect('/ketab')
    return response

class KetabCreateView(LoginRequiredMixin, CreateView):
    template_name = "ketab/ketab_create.html"
    form_class = KetabForm
    success_url = '/ketab'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        print(self.request.user)
        obj.save()
        return super(KetabCreateView, self).form_valid(form)


class KetabDetailView(LoginRequiredMixin, DetailView):
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



class KetabListView(LoginRequiredMixin,ListView):
    paginate_by = 4
    model = Ketab
    template_name = "ketab/ketab_list.html"



class KetabDeleteView(LoginRequiredMixin, DeleteView):
    model = Ketab
    template_name = "ketab/ketab_delete.html"
    success_url = reverse_lazy('ketab_list')


class KetabSearchView(LoginRequiredMixin, ListView):

    paginate_by = 4
    template_name = 'ketab/search_query.html'





    def is_valid_queryparam(self, param):
        print('is valid being run, param is: {}'.format(param))
        if param !="" and param is not None:
            return param

    def get_queryset(self):

        search_box_param = self.request.GET.get('q')

        tag_param = self.request.GET.get('tag')

        if self.is_valid_queryparam(search_box_param):
            qs = Ketab.objects.search(self.request.GET.get('q', None)).order_by('-created_date')
            return qs
        elif self.is_valid_queryparam(tag_param):
            qs = Ketab.objects.search_tags(self.request.GET.get('tag', None)).order_by('-created_date')
            return qs
        else:
            return Ketab.objects.all().order_by('-created_date')

    def get_context_data(self, **kwargs):


        context = super().get_context_data(**kwargs)

        context['common_tags'] = Ketab.tags.most_common()[:5]
        context['dist_tags'] = Ketab.tags.distinct()

        paginator = Paginator(self.get_queryset(), 3)

        page = self.request.GET.get('page')

        try:
            qs = paginator.page(page)
        except PageNotAnInteger:
            qs = paginator.page(1)
        except EmptyPage:
            qs = paginator.page(paginator.num_pages)

        except InvalidPage:
            qs = paginator.page(1)



        context['query_set'] = qs
        print(context)


        return context

