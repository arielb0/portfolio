from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

class Currency(models.Model):
    name = models.CharField(verbose_name = _('name'), unique = True, max_length = 32)
    code = models.CharField(verbose_name= _('code'), unique = True, max_length = 4)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return f'{self.name} ({self.code})'
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.name)
            
        return super().save()

    class Meta:
        verbose_name_plural = 'currencies'

class Category(models.Model):
    name = models.CharField(verbose_name = _('name'), unique = True, max_length = 32)
    picture = models.ImageField(verbose_name = _('picture'), upload_to = 'images/categories', blank=True, null=True)
    priority = models.IntegerField(verbose_name = _('priority'), blank=True, null=True)
    parent_category = models.ForeignKey('self', verbose_name = _('parent category'), on_delete = models.CASCADE, blank=True, null=True, related_name = 'subcategories')
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        if self.parent_category:
            return f'{self.parent_category} / {self.name}'
        
        return self.name

    def delete(self):
        if self.picture:
            self.picture.delete()

        super().delete()

    def save(self):

        if self.pk:
            old_model = Category.objects.get(pk = self.pk)
            if old_model.picture and old_model.picture != self.picture:
                old_model.picture.delete(save = False)
        else:
            self.slug = slugify(self.name)
        
        super().save()
    
    class Meta:
        verbose_name_plural = _('categories')
        ordering = ['priority']

class Ad(models.Model):
    title = models.CharField(verbose_name = _('title'), max_length = 64)
    description = models.CharField(verbose_name = _('description'), max_length = 4096)
    price = models.DecimalField(verbose_name = _('price'), max_digits = 10, decimal_places = 2)
    currency = models.ForeignKey(Currency, verbose_name = _('currency'), on_delete = models.CASCADE)
    date = models.DateField(verbose_name = _('date'), default=date.today)
    alternative_currencies = models.ManyToManyField(Currency, verbose_name=_('alternative currencies'), related_name = 'alternative_currencies', blank = True)
    category = models.ForeignKey(Category, verbose_name = _('category'), on_delete=models.CASCADE)
    moderator = models.ForeignKey(User, verbose_name = _('moderator'),on_delete = models.PROTECT, blank = True, null = True, related_name='moderator')
    PENDING = 0
    STATUS_CHOICES = {
        0: 'Pending',
        1: 'Rejected',
        2: 'Allowed'
    }
    status = models.IntegerField(verbose_name = _('status'), choices = STATUS_CHOICES, default = PENDING)
    picture_0 = models.ImageField(verbose_name = _("picture"), blank = True, upload_to='images/')
    picture_1 = models.ImageField(verbose_name = _('picture'), blank = True, upload_to='images/')
    picture_2 = models.ImageField(verbose_name = _('picture'), blank = True, upload_to='images/')
    picture_3 = models.ImageField(verbose_name = _('picture'), blank = True, upload_to='images/')
    picture_4 = models.ImageField(verbose_name = _('picture'), blank = True, upload_to='images/')
    picture_5 = models.ImageField(verbose_name = _('picture'), blank = True, upload_to='images/')
    picture_6 = models.ImageField(verbose_name = _('picture'), blank = True, upload_to='images/')
    picture_7 = models.ImageField(verbose_name = _('picture'), blank = True, upload_to='images/')
    picture_8 = models.ImageField(verbose_name = _('picture'), blank = True, upload_to='images/')
    picture_9 = models.ImageField(verbose_name = _('picture'), blank = True, upload_to='images/')
    rank = models.DecimalField(verbose_name = _('rank'), max_digits = 10, decimal_places = 2, default=0)
    owner = models.ForeignKey(User, verbose_name = _('owner'), on_delete=models.CASCADE, related_name='owner')
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return f'{self.currency.code} {self.price} {self.title}'
    
    def delete(self):

        for number in range(0, 10):
            field_name =  f'picture_{number}'
            picture = getattr(self, field_name)

            if picture:
                picture.delete()

        super().delete()

    def save(self):

        if self.pk:
            old_model = Ad.objects.get(pk=self.pk)
            
            for number in range(0, 10):
                field_name = f'picture_{number}'
                old_picture = getattr(old_model, field_name)
                new_picture = getattr(self, field_name)

                if old_picture and old_picture != new_picture:
                    old_picture.delete(save=False)
        else:
            self.slug = slugify(self.title)

        # TODO: For every picture field, create a thumbnail version..
        # self.status = self.PENDING If regular user save a model, otherwise preserve
        
        super().save()
    
    class Meta:
        ordering = ['-rank', '-date']
        permissions = [
            ('moderate_ad', 'Can moderate an Ad')
            ]

class Report(models.Model):
    REASON_CHOICES = {
        0: _('Forbidden'),
        1: _('Offensive'),
        2: _('Scam'),
        3: _('Wrong Category'),
        4: _('Joke'),
        5: _('Other Reason'),
    }
    reason = models.IntegerField(verbose_name = _('reason'), choices = REASON_CHOICES)
    description = models.CharField(verbose_name = _('description'), max_length = 254, blank = True)
    date = models.DateTimeField(verbose_name = _('date'), auto_now_add = True)
    readed = models.BooleanField(verbose_name = _('readed'), default = False)
    moderator = models.ForeignKey(User, verbose_name = _('moderator'), on_delete = models.PROTECT, blank = True, null = True)
    ad = models.OneToOneField(Ad, verbose_name = _('ad'), on_delete = models.CASCADE)

    def __str__(self):
        return f'{self.date} {self.reason} {self.ad}'
    
    def get_reason(self):
        return self.REASON_CHOICES[self.reason]
    
    class Meta:
        ordering = ['-date', '-reason']

class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name = _('user'), on_delete = models.CASCADE)
    address = models.CharField(verbose_name = _('address'), max_length = 64, blank = True)
    phone = models.CharField(verbose_name= _('phone'), max_length = 16, blank = True)

    def __str__(self):
        return self.user.username
    