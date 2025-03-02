from django.contrib.sitemaps import Sitemap
from .models import Category
from .models import Ad
from django.urls import reverse

class AbstractSitemap(Sitemap):
    protocol = 'https'

class CategorySitemap(AbstractSitemap):    
    changefreq = 'daily'
    priority = 0.5

    def items(self):
        return Category.objects.filter(subcategories = None)
    
class AdSitemap(AbstractSitemap):
    changefreq = 'daily'
    priority = 0.9

    def items(self):
        return Ad.objects.all()
    
class StaticViewSitemap(AbstractSitemap):
    changefreq = 'monthly'
    priority = 0.5
    
    def items(self):
        return ['bazaar:home', 'bazaar:terms_and_conditions', 'bazaar:about_us', 'bazaar:privacy_policy']
    
    def location(self, item):
        return reverse(item)