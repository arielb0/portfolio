from django.urls import path
from .views import CreateCurrency, DetailCurrency, UpdateCurrency, DeleteCurrency, ListCurrency
from .views import CreateCategory, DetailCategory, UpdateCategory, DeleteCategory, ListCategory
from .views import CreateAd, DetailAd, UpdateAd, DeleteAd, ListAd, UpdateAdStatus, ListPendingAd, ListRejectedAd
from .views import CreateReport, DetailReport, UpdateReport, DeleteReport, ListReport
from .views import DetailProfile, UpdateProfile
from .views import Home
from .views import UpdateUserProfile
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

app_name = 'bazaar'

urlpatterns = [
    path('currency/create', CreateCurrency.as_view(), name = 'currency_create'),
    path('currency/<int:pk>', DetailCurrency.as_view(), name = 'currency_detail'),
    path('currency/<int:pk>/update', UpdateCurrency.as_view(), name = 'currency_update'),
    path('currency/<int:pk>/delete', DeleteCurrency.as_view(), name = 'currency_delete'),
    path('currency', ListCurrency.as_view(), name = 'currency_list'),
    path('category/create', CreateCategory.as_view(), name = 'category_create'),
    path('category/<int:pk>', DetailCategory.as_view(), name = 'category_detail'),
    path('category/<int:pk>/update', UpdateCategory.as_view(), name = 'category_update'),
    path('category/<int:pk>/delete', DeleteCategory.as_view(), name = 'category_delete'),
    path('category', ListCategory.as_view(), name = 'category_list'),
    path('create', CreateAd.as_view(), name='ad_create'),
    path('<int:pk>', DetailAd.as_view(), name='ad_detail'),
    path('<int:pk>/update', UpdateAd.as_view(), name='ad_update'),
    path('<int:pk>/delete', DeleteAd.as_view(), name='ad_delete'),
    path('search', ListAd.as_view(), name='ad_list'),
    path('report/create/ad/<int:pk>', CreateReport.as_view(), name='report_create'),
    path('report/<int:pk>', DetailReport.as_view(), name='report_detail'),
    path('report/<int:pk>/update', UpdateReport.as_view(), name='report_update'),
    path('report/<int:pk>/delete', DeleteReport.as_view(), name='report_delete'),
    path('report/', ListReport.as_view(), name='report_list'),    
    path('profile/', DetailProfile.as_view(), name='profile_detail'),
    path('profile/update', UpdateProfile.as_view(), name = 'profile_update'),
    path('user/update', UpdateUserProfile.as_view(), name='profile_user_update'),
    path('password/update', PasswordChangeView.as_view(success_url = reverse_lazy('bazaar:profile_detail'), template_name = 'bazaar/profile_form.html'), name = 'profile_password_update'),
    path('<int:pk>/moderate', UpdateAdStatus.as_view(), name='ad_moderate'),
    path('pending', ListPendingAd.as_view(), name='ad_pending'),
    path('rejected', ListRejectedAd.as_view(), name='ad_rejected'),
    path('', Home.as_view(), name='home')
]