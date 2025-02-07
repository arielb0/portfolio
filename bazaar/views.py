from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView, TemplateView
from .models import Currency, Category, Ad, Report, Profile
from .forms import CurrencyForm, CategoryForm, AdForm, AdStatusForm, ReportForm, ProfileForm, AdvancedSearchForm
from accounts.forms import UserAdminForm, UserForm
from accounts.views import UpdateUser
from django.urls import reverse_lazy
from django.db.models import Q
from .helpers import normalize_ad_pictures, get_simple_search_form
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext_lazy as _

# Create your views here.

class CreateCurrency(UserPassesTestMixin, CreateView):
    model = Currency
    form_class = CurrencyForm
    success_url = reverse_lazy('bazaar:currency_list')

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)        
        context = get_simple_search_form(context)
        return context

    def test_func(self) -> bool | None:
        return self.request.user.is_superuser or self.request.user.has_perm('bazaar.add_currency')

class DetailCurrency(UserPassesTestMixin, DetailView):
    model = Currency

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context = get_simple_search_form(context)
        return context

    def test_func(self) -> bool | None:
        return self.request.user.is_superuser or self.request.user.has_perm('bazaar.view_currency')

class UpdateCurrency(UserPassesTestMixin, UpdateView):
    model = Currency
    form_class = CurrencyForm
    success_url = reverse_lazy('bazaar:currency_list')

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context = get_simple_search_form(context)
        return context

    def test_func(self) -> bool | None:
        return self.request.user.is_superuser or self.request.user.has_perm('bazaar.change_currency')

class DeleteCurrency(UserPassesTestMixin, DeleteView):
    model = Currency
    success_url = reverse_lazy('bazaar:currency_list')

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context = get_simple_search_form(context)
        return context

    def test_func(self) -> bool | None:
        return self.request.user.is_superuser or self.request.user.has_perm('bazaar.delete_currency')
    

class ListCurrency(UserPassesTestMixin, ListView):
    model = Currency

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context = get_simple_search_form(context)
        return context
    
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.has_perm('bazaar.view_currency')        
    

class CreateCategory(UserPassesTestMixin, CreateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('bazaar:category_list')

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context = get_simple_search_form(context)
        return context
    
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.has_perm('bazaar.add_category')
    

class DetailCategory(UserPassesTestMixin, DetailView):
    model = Category

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context = get_simple_search_form(context)
        return context
    
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.has_perm('bazaar.view_category')
    

class UpdateCategory(UserPassesTestMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('bazaar:category_list')

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context = get_simple_search_form(context)
        return context
    
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.has_perm('bazaar.change_category')
    

class DeleteCategory(UserPassesTestMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('bazaar:category_list')

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context = get_simple_search_form(context)
        return context
    
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.has_perm('bazaar.delete_category')
    

class ListCategory(UserPassesTestMixin, ListView):
    model = Category

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context = get_simple_search_form(context)
        return context
    
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.has_perm('bazaar.view_category')
    

class CreateAd(LoginRequiredMixin, CreateView):
    model = Ad
    form_class = AdForm
    success_url = reverse_lazy('bazaar:ad_list')

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)        
        context = get_simple_search_form(context)
        return context

    def post(self, request: HttpRequest, *args: str, **kwargs) -> HttpResponse:        
        self.request = normalize_ad_pictures(request, (748, 420)) # TODO: You need to use self.request.POST = self.request.POST.copy()
        return super().post(request, *args, **kwargs)
    
    def form_valid(self, form):
        self.object = form.save(commit = False)
        self.object.owner = self.request.user
        self.object.save()
        
        return HttpResponseRedirect(self.get_success_url())
    

class DetailAd(DetailView):
    model = Ad

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context = get_simple_search_form(context)
        return context
    

class UpdateAd(UserPassesTestMixin, UpdateView):
    model = Ad
    form_class = AdForm
    success_url = reverse_lazy('bazaar:ad_list')

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context = get_simple_search_form(context)
        return context

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        self.request = normalize_ad_pictures(request, (748, 420)) # TODO: You need to use self.request.POST = self.request.POST.copy().
        return super().post(request, *args, **kwargs)

    
    def form_valid(self, form):
        
        if not (self.request.user.is_superuser or self.request.user.groups.filter(Q(name = 'Bazaar Superuser') | Q(name = 'Bazaar Moderator')).exists()):
            ad = form.save(commit = False)
            ad.status = 0 # Pending status..
            ad.save()
        else:
            form.save(commit = True)

        return HttpResponseRedirect(self.get_success_url())
    
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.has_perm('bazaar.change_ad') or self.get_object().owner == self.request.user


class DeleteAd(UserPassesTestMixin, DeleteView):
    model = Ad
    success_url = reverse_lazy('bazaar:ad_list')

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context = get_simple_search_form(context)
        return context
    
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.has_perm('bazaar.delete_ad') or self.get_object().owner == self.request.user
    

class ListAd(ListView):
    model = Ad

    def get_queryset(self):

        if 'my_ads' not in self.request.GET.keys():
            queryset = Ad.objects.filter(status = 2)
        else:
            queryset = Ad.objects.all()

        keyword_queryset = self.request.GET.get('query', '')
        price_start = self.request.GET.get('price_start', '')
        price_end = self.request.GET.get('price_end', '')
        currencies = self.request.GET.getlist('currencies', [])
        date_start = self.request.GET.get('date_start', '')
        date_end = self.request.GET.get('date_end', '')
        category = self.request.GET.get('category', '')
        my_ads = self.request.GET.get('my_ads', '')

        if keyword_queryset:
            queryset = queryset.filter(Q(title__icontains=keyword_queryset) | Q(description__icontains=keyword_queryset))
        
        if price_start:
            queryset = queryset.filter(Q(price__gte=price_start))

        if price_end:
            queryset = queryset.filter(Q(price__lte=price_end))

        if currencies:
            currencies = self.request.GET.getlist('currencies')
            currency_query = Q(currency__slug=currencies[0])

            for currency in currencies[1:]:
                currency_query = Q(currency_query | Q(alternative_currencies__slug=currency))

            queryset = queryset.filter(currency_query).distinct()

        if date_start:
            queryset = queryset.filter(Q(date__gte=date_start))

        if date_end:
            queryset = queryset.filter(Q(date__lte=date_end))
        
        if category:
            queryset = queryset.filter(Q(category__slug=category))

        if my_ads:
            queryset = queryset.filter(Q(owner=self.request.user))
        
        return queryset

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context = get_simple_search_form(context, self.request.GET)
        context['advanced_search_form'] = AdvancedSearchForm(data = self.request.GET)

        get_keys = self.request.GET.keys()
        
        if 'query' in get_keys and self.request.GET.get('query') != '':
            context['breadcrumb_current_page'] = _(f'Search results for "{self.request.GET.get("query")}"')

        if 'category' in get_keys and self.request.GET.get('category') != '':
            context['breadcrumb_current_page'] = Category.objects.get(slug = self.request.GET.get('category'))

        if 'my_ads' in get_keys:
            context['breadcrumb_current_page'] = _('My Ads')

        if 'price_start' in get_keys or 'price_end' in get_keys \
            or 'currency' in get_keys or 'address' in get_keys \
            or 'date_start' in get_keys or 'date_end' in get_keys:

            context['breadcrumb_current_page'] = _('Advanced Search')

        context['breadcrumb_current_page'] = _('Search results')
        
        return context
        
    
class UpdateAdStatus(UpdateAd):
    form_class = AdStatusForm
    success_url = reverse_lazy('bazaar:ad_pending')

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.has_perm('bazaar.moderate_ad')
    

class ListPendingAd(UserPassesTestMixin, ListAd):

    def get_template_names(self):
        return ['bazaar/ad_pending_list.html']

    def get_queryset(self):
        return Ad.objects.filter(status = 0)

    def test_func(self):        
        return self.request.user.is_superuser or self.request.user.has_perm('bazaar.moderate_ad')
        

class ListRejectedAd(UserPassesTestMixin, ListAd):

    def get_template_names(self):
        return ['bazaar/ad_rejected_list.html']

    def get_queryset(self):
        return Ad.objects.filter(status = 1)

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.has_perm('bazaar.moderate_ad')


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
    
    def get_success_url(self):
        if self.request.user.is_superuser or self.request.user.has_perm('bazaar.view_report'):
            return self.success_url
        
        return reverse_lazy('bazaar:ad_list')

class DetailReport(UserPassesTestMixin, DetailView):
    model = Report

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context = get_simple_search_form(context)
        return context
    
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.has_perm('bazaar.view_report')

class UpdateReport(UserPassesTestMixin, UpdateView): # You don't need to update a report. Only read and delete
    model = Report
    form_class = ReportForm
    success_url = reverse_lazy('bazaar:report_list')

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context = get_simple_search_form(context)
        return context
    
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.has_perm('bazaar.view_report')

class DeleteReport(UserPassesTestMixin, DeleteView):
    model = Report
    success_url = reverse_lazy('bazaar:report_list')

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context = get_simple_search_form(context)
        return context
    
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.has_perm('bazaar.view_report')

class ListReport(UserPassesTestMixin, ListView):
    model = Report

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context = get_simple_search_form(context)
        return context
    
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.has_perm('bazaar.view_report')
    
class DetailProfile(DetailView):
    model = Profile

    def get_object(self):
        return Profile.objects.get_or_create(user = self.request.user)[0]

class UpdateProfile(UpdateView):
    model = Profile
    form_class = ProfileForm
    success_url = reverse_lazy('bazaar:profile_detail')
    
    def get_object(self, **kwargs):
        return Profile.objects.get_or_create(user = self.request.user)[0]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        if self.request.user.is_superuser:
            context['user_form'] = UserAdminForm(instance = self.request.user)
        else:
            context['user_form'] = UserForm(instance = self.request.user)
        context['password_form'] = PasswordChangeForm(user = self.request.user)
        return context

class UpdateUserProfile(UpdateUser):
    success_url = reverse_lazy('bazaar:profile_detail')

    def get_object(self):
        return self.request.user
    
class Home(TemplateView):
    template_name = 'bazaar/home.html'

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        context['object_list'] = Category.objects.all()
        context = get_simple_search_form(context)
       
        return context
    
class TermsAndConditions(TemplateView):
    template_name = 'bazaar/terms_and_conditions.html'

class AboutUs(TemplateView):
    template_name = 'bazaar/about_us.html'

class PrivacyPolicy(TemplateView):
    template_name = 'bazaar/privacy_policy.html'
