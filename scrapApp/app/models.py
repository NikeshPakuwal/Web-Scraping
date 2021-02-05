from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from django.urls import reverse

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
