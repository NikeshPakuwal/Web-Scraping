from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from django.urls import reverse

from django_countries.fields import CountryField

try:
    from django.db.models import JSONField
except ImportError:
    from django.contrib.postgres.fields import JSONField

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    skill = models.CharField(max_length=255)
    location = models.TextField()

    def __str__(self):
        return self.first_name

class Semrush(models.Model):
    objects = None
    Item = None
    country = models.CharField(max_length=255, blank=True, null=True)
    keyword = models.CharField(max_length=255, blank=True, null=True)
    seed_keyword = models.CharField(max_length=255, blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, null=True)
    volume = models.IntegerField(blank=True, null=True)
    keyword_difficulty = models.CharField(max_length=255, blank=True, null=True)
    ccp = models.CharField(max_length=255, blank=True, null=True)
    competitive_density = models.CharField(max_length=255, blank=True, null=True)
    number_of_results = models.CharField(max_length=255, blank=True, null=True)
    serp_Features = models.TextField(blank=True, null=True)
    trend = models.CharField(max_length=255, blank=True, null=True)
    click_potential = models.CharField(max_length=255, blank=True, null=True)
    competitors = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.country+" "+self.seed_keyword


class ScrapWeb(models.Model):
    title = models.TextField()
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        default_permissions = ('add',)
        permissions = (('give_refund', 'Can refund customers'), ('can_hire', 'Can hire employees'))

    def __str__(self):
        return self.title

class UploadGoogleDataLink(models.Model):
    keyword_id = models.ForeignKey(Semrush, on_delete=models.CASCADE)
    links = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        default_permissions = ('add',)
        permissions = (('give_refund', 'Can refund customers'), ('can_hire', 'Can hire employees'))

    def __str__(self):
        return self.keyword_id

class ScrapGoogleDataLinkData(models.Model):
    #keyword_id = models.ForeignKey(UploadGoogleDataLink, on_delete=models.CASCADE)
    keyword_id = models.IntegerField()
    title = models.TextField()
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        default_permissions = ('add',)
        permissions = (('give_refund', 'Can refund customers'), ('can_hire', 'Can hire employees'))

    def get_absolute_url(self):
        return reverse('ScrapGoogleDataLinkData')



# Scrap Data Model
class ScrapData(models.Model):
    country = CountryField(multiple=True)

    def __str__(self):
        return self.country



#json data store
class StoreJsonData(models.Model):
    title = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    images = models.TextField(blank=True, null=True)
    source = JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    born = models.TextField(blank=True, null=True)
    height = models.TextField(blank=True, null=True)
    books = models.TextField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    children = models.TextField(blank=True, null=True)
    known_attributes = models.TextField(blank=True, null=True)
    profiles = models.TextField(blank=True, null=True)
    people_also_search_for = models.TextField(blank=True, null=True)
    related_searches = models.TextField(blank=True, null=True)
    related_questions = models.TextField(blank=True, null=True)
    organic_results = models.TextField(blank=True, null=True)
    pagination = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title