from django.http import HttpRequest, HttpResponse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView, TemplateView
from .models import Currency, Category, Ad, Report
from .forms import CurrencyForm, CategoryForm, AdForm, ReportForm, AdvancedSearchForm
from django.urls import reverse_lazy
from django.db.models import Q
from .helpers import normalize_ad_pictures, get_simple_search_form


# Create your views here.

class CreateCurrency(CreateView):
    model = Currency
    form_class = CurrencyForm
    success_url = reverse_lazy('bazaar:currency_list')

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)        
        context = get_simple_search_form(context)
        return context
    

class DetailCurrency(DetailView):
    model = Currency

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context = get_simple_search_form(context)
        return context
    

class UpdateCurrency(UpdateView):
    model = Currency
    form_class = CurrencyForm
    success_url = reverse_lazy('bazaar:currency_list')

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context = get_simple_search_form(context)
        return context
    

class DeleteCurrency(DeleteView):
    model = Currency
    success_url = reverse_lazy('bazaar:currency_list')

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context = get_simple_search_form(context)
        return context
    

class ListCurrency(ListView):
    model = Currency

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context = get_simple_search_form(context)
        return context
    

class CreateCategory(CreateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('bazaar:category_list')

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context = get_simple_search_form(context)
        return context

class DetailCategory(DetailView):
    model = Category

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context = get_simple_search_form(context)
        return context

class UpdateCategory(UpdateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('bazaar:category_list')

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context = get_simple_search_form(context)
        return context

class DeleteCategory(DeleteView):
    model = Category
    success_url = reverse_lazy('bazaar:category_list')

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context = get_simple_search_form(context)
        return context

class ListCategory(ListView):
    model = Category

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context = get_simple_search_form(context)
        return context

class CreateAd(CreateView):
    model = Ad
    form_class = AdForm
    success_url = reverse_lazy('bazaar:ad_list')

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)        
        context = get_simple_search_form(context)
        return context

    def post(self, request: HttpRequest, *args: str, **kwargs) -> HttpResponse:        
        self.request = normalize_ad_pictures(request, (748, 420))
        return super().post(request, *args, **kwargs)

class DetailAd(DetailView):
    model = Ad

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context = get_simple_search_form(context)
        return context

class UpdateAd(UpdateView):
    model = Ad
    form_class = AdForm
    success_url = reverse_lazy('bazaar:ad_list')

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context = get_simple_search_form(context)
        return context

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        self.request = normalize_ad_pictures(request, (748, 420))
        return super().post(request, *args, **kwargs)    

class DeleteAd(DeleteView):
    model = Ad
    success_url = reverse_lazy('bazaar:ad_list')

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context = get_simple_search_form(context)
        return context

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

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context = get_simple_search_form(context, self.request.GET)
        context['advanced_search_form'] = AdvancedSearchForm(data = self.request.GET)
    
        return context
        

class CreateReport(CreateView):
    model = Report
    form_class = ReportForm
    success_url = reverse_lazy('bazaar:report_list')

    def get_initial(self):
        initial = super().get_initial()        
        initial['ad'] = self.kwargs['pk']
        return initial

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context = get_simple_search_form(context)
        return context

class DetailReport(DetailView):
    model = Report

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context = get_simple_search_form(context)
        return context

class UpdateReport(UpdateView):
    model = Report
    form_class = ReportForm
    success_url = reverse_lazy('bazaar:report_list')

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context = get_simple_search_form(context)
        return context

class DeleteReport(DeleteView):
    model = Report
    success_url = reverse_lazy('bazaar:report_list')

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context = get_simple_search_form(context)
        return context

class ListReport(ListView):
    model = Report

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context = get_simple_search_form(context)
        return context

class Home(TemplateView):
    template_name = 'bazaar/home.html'

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        context['object_list'] = Category.objects.all()
        context = get_simple_search_form(context)
       
        return context
