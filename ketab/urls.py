from django.urls import path
from . import views




#create
#read
#update
#delete

urlpatterns = [
    path('create/', views.KetabCreateView.as_view(), name='ketab_create'),
    path('<str:slug>-<int:pk>/detail', views.KetabDetailView.as_view(), name = 'ketab_detail'),
    path('<str:slug>-<int:pk>/edit/', views.KetabUpdateView.as_view(), name='ketab_update'),
    path('', views.KetabListView.as_view(), name='ketab_list'),
    path('<str:slug>-<int:pk>/delete/', views.KetabDeleteView.as_view(), name='ketab_list'),
    path('search/', views.KetabSearchView.as_view(), name = 'ketab_search')

]
