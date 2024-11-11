from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

class Currency(models.Model):
    name = models.CharField(unique = True, max_length = 32)
    code = models.CharField(unique = True, max_length = 4)

    def __str__(self):
        return f'{self.name} ({self.code})'

    class Meta:
        verbose_name_plural = 'currencies'

class Category(models.Model):
    name = models.CharField(unique = True, max_length = 32)
    picture = models.ImageField(upload_to = 'images/categories', blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    parent_category = models.ForeignKey('self', on_delete = models.CASCADE, blank=True, null=True, related_name = 'subcategories')

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
        
        super().save()
    
    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['-priority']

class Ad(models.Model):
    title = models.CharField(max_length = 64)
    description = models.CharField(max_length = 254)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    currency = models.ForeignKey(Currency, on_delete = models.CASCADE)
    date = models.DateField(default=date.today)
    alternative_currencies = models.ManyToManyField(Currency, related_name = 'alternative_currencies', blank = True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    moderator = models.ForeignKey(User, on_delete = models.PROTECT, blank = True, null = True)
    PENDING = 0
    STATUS_CHOICES = {
        0: 'Pending',
        1: 'Rejected',
        2: 'Allowed'
    }
    status = models.IntegerField(choices = STATUS_CHOICES, default = PENDING)
    picture_0 = models.ImageField(blank = True, upload_to='images/')
    picture_1 = models.ImageField(blank = True, upload_to='images/')
    picture_2 = models.ImageField(blank = True, upload_to='images/')
    picture_3 = models.ImageField(blank = True, upload_to='images/')
    picture_4 = models.ImageField(blank = True, upload_to='images/')
    picture_5 = models.ImageField(blank = True, upload_to='images/')
    picture_6 = models.ImageField(blank = True, upload_to='images/')
    picture_7 = models.ImageField(blank = True, upload_to='images/')
    picture_8 = models.ImageField(blank = True, upload_to='images/')
    picture_9 = models.ImageField(blank = True, upload_to='images/')
    rank = models.DecimalField(max_digits = 10, decimal_places = 2, default=0)

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
        
        super().save()
    
    class Meta:
        ordering = ['-rank', '-date']

class Report(models.Model):
    REASON_CHOICES = {
        0: 'Forbidden',
        1: 'Offensive',
        2: 'Scam',       
        3: 'Wrong Category',
        4: 'Joke',
        5: 'Other Reason',
    }
    reason = models.IntegerField(choices = REASON_CHOICES)
    description = models.CharField(max_length = 254, blank = True)
    date = models.DateTimeField(auto_now_add = True)
    readed = models.BooleanField(default = False)
    moderator = models.ForeignKey(User, on_delete = models.PROTECT, blank = True, null = True)
    ad = models.OneToOneField(Ad, on_delete = models.CASCADE)

    def __str__(self):
        return f'{self.date} {self.reason} {self.ad}'
    
    def get_reason(self):
        return self.REASON_CHOICES[self.reason]
    
    class Meta:
        ordering = ['-date', '-reason']

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length = 64, blank = True)
    phone = models.CharField(max_length = 16, blank = True)

    def __str__(self):
        return self.user.username