from django.http import HttpRequest, HttpResponse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView, TemplateView
from .models import Currency, Category, Ad, Report
from .forms import CurrencyForm, CategoryForm, AdForm, ReportForm
from django.urls import reverse_lazy
from django.db.models import Q
from .helpers import normalize_ad_pictures

# Create your views here.

class CreateCurrency(CreateView):
    model = Currency
    form_class = CurrencyForm
    success_url = reverse_lazy('bazaar:currency_list')

class DetailCurrency(DetailView):
    model = Currency

class UpdateCurrency(UpdateView):
    model = Currency
    form_class = CurrencyForm
    success_url = reverse_lazy('bazaar:currency_list')

class DeleteCurrency(DeleteView):
    model = Currency
    success_url = reverse_lazy('bazaar:currency_list')

class ListCurrency(ListView):
    model = Currency

class CreateCategory(CreateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('bazaar:category_list')

class DetailCategory(DetailView):
    model = Category

class UpdateCategory(UpdateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('bazaar:category_list')

class DeleteCategory(DeleteView):
    model = Category
    success_url = reverse_lazy('bazaar:category_list')

class ListCategory(ListView):
    model = Category

class CreateAd(CreateView):
    model = Ad
    form_class = AdForm
    success_url = reverse_lazy('bazaar:ad_list')

    def post(self, request: HttpRequest, *args: str, **kwargs) -> HttpResponse:        
        self.request = normalize_ad_pictures(request, (748, 420))
        return super().post(request, *args, **kwargs)

class DetailAd(DetailView):
    model = Ad

class UpdateAd(UpdateView):
    model = Ad
    form_class = AdForm
    success_url = reverse_lazy('bazaar:ad_list')

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        self.request = normalize_ad_pictures(request, (748, 420))
        return super().post(request, *args, **kwargs)    

class DeleteAd(DeleteView):
    model = Ad
    success_url = reverse_lazy('bazaar:ad_list')

class ListAd(ListView):
    model = Ad

    def get_queryset(self):

        queryset = super().get_queryset()

        currency_queryset = self.request.GET.get('query', '')
        price_start = self.request.GET.get('price_start', '')
        price_end = self.request.GET.get('price_end', '')
        currencies = self.request.GET.getlist('currencies', [])
        address = self.request.GET.get('address', '')
        date_start = self.request.GET.get('date_start', '')
        date_end = self.request.GET.get('date_end', '')
        category = self.request.GET.get('category', '')

        if currency_queryset:
            queryset = queryset.filter(Q(title__icontains=currency_queryset) | Q(description__icontains=currency_queryset))

        if price_start:
            queryset = queryset.filter(Q(price__gte=price_start))

        if price_end:
            queryset = queryset.filter(Q(price__lte=price_end))

        if currencies:
            currencies = self.request.GET.getlist('currencies')
            currency_queryset = Q(currency=currencies[0])

            for currency in currencies[1:]:
                currency_queryset = Q(currency_queryset | Q(alternative_currencies=currency))

            queryset = queryset.filter(currency_queryset).distinct()

        if address:
            queryset = queryset.filter(Q(address__icontains=address))

        if date_start:
            queryset = queryset.filter(Q(date__gte=date_start))

        if date_end:
            queryset = queryset.filter(Q(date__lte=date_end))
        
        if category:
            queryset = queryset.filter(Q(category=category))
        
        return queryset
        '''
        if len(self.request.GET.keys()) != 0:
            
            if 'keyword' in self.request.GET.keys() and self.request.GET['keyword'] != '': 
                queryset = queryset.filter(Q(title__icontains=self.request.GET['keyword']) | Q(description__icontains=self.request.GET['keyword']))
            
            if 'price_start' in self.request.GET.keys() and self.request.GET['price_start'] != '':
                queryset = queryset.filter(price__gte=self.request.GET['price_start'])

            if 'price_end' in self.request.GET.keys() and self.request.GET['price_end'] != '':
                queryset = queryset.filter(price__lte=self.request.GET['price_end'])

            if 'currencies' in self.request.GET.keys() and len(self.request.GET.getlist('currencies')) > 0:

                currencies = self.request.GET.getlist('currencies')
                query = Q(currency=currencies[0])

                for currency in currencies[1:]:
                    query = Q(query | Q(alternative_currencies=currency))

                queryset = queryset.filter(query).distinct()

            if 'address' in self.request.GET.keys() and self.request.GET['address'] != '':
                queryset = queryset.filter(address__contains=self.request.GET['address'])

            if 'date_start' in self.request.GET.keys() and self.request.GET['date_start'] != '':
                queryset = queryset.filter(date__gte=self.request.GET['date_start'])

            if 'date_end' in self.request.GET.keys() and self.request.GET['date_end'] != '':
                queryset = queryset.filter(date__lte=self.request.GET['date_end'])

            if 'category' in self.request.GET.keys() and self.request.GET['category'] != '':
                queryset = queryset.filter(category=self.request.GET['category'])
        
        return queryset
        '''
    '''
    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        print(f'This is the GET keys on the view: {self.request.GET}')
        print(f'This is the context of search page (ad_list): {context}')
        return context
    '''

class CreateReport(CreateView):
    model = Report
    form_class = ReportForm
    success_url = reverse_lazy('bazaar:report_list')

    def get_initial(self):
        initial = super().get_initial()        
        initial['ad'] = self.kwargs['pk']
        return initial

class DetailReport(DetailView):
    model = Report

class UpdateReport(UpdateView):
    model = Report
    form_class = ReportForm
    success_url = reverse_lazy('bazaar:report_list')

class DeleteReport(DeleteView):
    model = Report
    success_url = reverse_lazy('bazaar:report_list')

class ListReport(ListView):
    model = Report

class Home(TemplateView):
    template_name = 'bazaar/home.html'

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        context['object_list'] = Category.objects.all()
        
        return context
