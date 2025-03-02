from django.urls import path
from .views import CreateCurrency, DetailCurrency, UpdateCurrency, DeleteCurrency, ListCurrency
from .views import CreateCategory, DetailCategory, UpdateCategory, DeleteCategory, ListCategory
from .views import CreateAd, DetailAd, UpdateAd, DeleteAd, ListAd, UpdateAdStatus, ListPendingAd, ListRejectedAd
from .views import CreateReport, DetailReport, UpdateReport, DeleteReport, ListReport
from .views import DetailProfile, UpdateProfile
from .views import Home, TermsAndConditions, AboutUs, PrivacyPolicy
from .views import UpdateUserProfile
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.sitemaps.views import sitemap
from .sitemaps import CategorySitemap, AdSitemap, StaticViewSitemap

app_name = 'bazaar'

urlpatterns = [
    path('currency/create', CreateCurrency.as_view(), name = 'currency_create'),
    path('currency/<slug:slug>/detail', DetailCurrency.as_view(), name = 'currency_detail'),
    path('currency/<slug:slug>/update', UpdateCurrency.as_view(), name = 'currency_update'),
    path('currency/<slug:slug>/delete', DeleteCurrency.as_view(), name = 'currency_delete'),
    path('currency', ListCurrency.as_view(), name = 'currency_list'),
    path('category/create', CreateCategory.as_view(), name = 'category_create'),
    path('category/<slug:slug>/detail', DetailCategory.as_view(), name = 'category_detail'),
    path('category/<slug:slug>/update', UpdateCategory.as_view(), name = 'category_update'),
    path('category/<slug:slug>/delete', DeleteCategory.as_view(), name = 'category_delete'),
    path('category', ListCategory.as_view(), name = 'category_list'),
    path('ad/create', CreateAd.as_view(), name='ad_create'),
    path('ad/<slug:slug>/detail', DetailAd.as_view(), name='ad_detail'),
    path('ad/<slug:slug>/update', UpdateAd.as_view(), name='ad_update'),
    path('ad/<slug:slug>/delete', DeleteAd.as_view(), name='ad_delete'),
    path('ad', ListAd.as_view(), name='ad_list'),
    path('ad/<slug:slug>/moderate', UpdateAdStatus.as_view(), name='ad_moderate'),
    path('ad/pending', ListPendingAd.as_view(), name='ad_pending'),
    path('ad/rejected', ListRejectedAd.as_view(), name='ad_rejected'),
    path('report/create/ad/<int:pk>', CreateReport.as_view(), name='report_create'),
    path('report/<int:pk>', DetailReport.as_view(), name='report_detail'),
    path('report/<int:pk>/update', UpdateReport.as_view(), name='report_update'),
    path('report/<int:pk>/delete', DeleteReport.as_view(), name='report_delete'),
    path('report/', ListReport.as_view(), name='report_list'),
    path('profile/detail', DetailProfile.as_view(), name='profile_detail'),
    path('profile/update', UpdateProfile.as_view(), name = 'profile_update'),
    path('user/update', UpdateUserProfile.as_view(), name='profile_user_update'),
    path('password/update', PasswordChangeView.as_view(success_url = reverse_lazy('bazaar:profile_detail'), template_name = 'bazaar/profile_form.html'), name = 'profile_password_update'),
    path('', Home.as_view(), name='home'),
    path('terms-and-conditions', TermsAndConditions.as_view(), name='terms_and_conditions'),
    path('about-us', AboutUs.as_view(), name='about_us'),
    path('privacy-policy', PrivacyPolicy.as_view(), name='privacy_policy'),
    path('sitemap.xml', sitemap, {'sitemaps': { 'static':  StaticViewSitemap ,'category': CategorySitemap, 'ad': AdSitemap }}, name = 'django.contrib.sitemaps.views.sitemap')
]