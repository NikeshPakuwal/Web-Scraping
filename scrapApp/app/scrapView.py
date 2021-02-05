from bs4 import BeautifulSoup
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView
from datatables_view.views import DatatablesView
from django.views import View
from .forms import ScrapForm
from .models import ScrapGoogleDataLinkData
from django.urls import reverse_lazy
import requests, urllib
from django.http import HttpResponse, JsonResponse
import pprint

class ScrapList(View):

    def get(self, request):
        title = 'Semrush Data List'
        context = {
            'title': title,
        }
        template_name = 'admin/scraping/list.html'
        return render(request, template_name, context)

class scrap_list_json(DatatablesView):
    model = ScrapGoogleDataLinkData
    title = 'Semrush'

    column_defs = [
        {
            'name': 'id',

        },
        {
            'name': 'keyword_id',
        }, {
            'name': 'title',
        }, {
            'name': 'created_date',
        },{
            'name': 'Action',
            'searchable': False
        }
    ]

    def customize_row(self, row, obj):

        row[
            'Action'] = '<a class="btn btn-primary" href="%s">%s</a> <a data-url="%s" class="btn btn-danger delete_button">%s</a>' % (
            reverse_lazy('scrap_links', args=(obj.id,)),
            'View',
            reverse_lazy('semrush_delete', args=(obj.id,)),
            '<i class="fas fa-trash-alt"></i>'
        )

        return

class scrapDataView(DetailView):
    title = 'Scrap Data View'
    queryset = ScrapGoogleDataLinkData.objects.all()

    template_name = 'admin/scraping/view.html'


    def get_object(self):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(ScrapGoogleDataLinkData, id=id_)




def djbs(request):
    title = 'Link Scraping'
    # Proxies api-endpoint
    URL = "http://api.proxiesapi.com"

    auth_key = "8aaf4535c3d7b6e0efd39ffe898f6efa_sr98766_ooPq87"
    session = "444"

    if request.method == "POST":
        # form = ScrapForm(request.POST, request.FILES)


        page_url = request.POST.get('web_link', None)

        PARAMS = {'auth_key': auth_key, 'url': page_url, 'render': 'true'}

        r = requests.get(url=URL, params=PARAMS)

        html = BeautifulSoup(r.content, 'html.parser')

        metadata = {
            'title': get_title(html),
            'description': get_description(html),
        }
        result = metadata

        return render(request, 'admin/scraping/django-bs.html', {'result': result})
    else:
        form = ScrapForm()
        context = {
            'title': title,
            'form': form
        }
    return render(request, 'admin/scraping/django-bs.html', context)


class DjBs(TemplateView):
    # title = 'Link Scraping'
    template_name = "admin/scraping/django-bs.html"

    def post(self, request, *args, **kwargs):

        website_link = request.POST.get('web_link', None)

        # requests
        url = website_link
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}  # headers
        source = requests.get(url, headers=headers)

        # beautifulsoup
        soup = BeautifulSoup(source, 'html.parser')

        # check if <h1> element is found
        if soup:
            result = soup.text

        else:
            result = "H1 Element is not found"

        return render(request, 'django-bs.html', {'result': result})


def get_title(html):
    """Scrape page title."""
    title = None
    if html.title.string:
        title = html.title.string
    elif html.find("meta", property="og:title"):
        title = html.find("meta", property="og:title").get('content')
    elif html.find("meta", property="twitter:title"):
        title = html.find("meta", property="twitter:title").get('content')
    elif html.find("h1"):
        title = html.find("h1").string
    return title


def get_description(html):
    """Scrape page description."""
    description = None
    if html.find("article"):
        description = html.find("article")
    elif html.find("div", {'class': ['wrap-content-main', 'post_the_content', 'mw-parser-output', 'descContainer', 'content']}):
        description = html.find(True, {'class': ['wrap-content-main', 'mw-parser-output', 'post_the_content', 'descContainer', 'content']})
    elif html.find("main", id_='main'):
        description = html.find("main")
    elif html.find("p"):
        description = html.body.find_all('p')

    # description = html.find(True, {'class':['wrap-content-main', 'post_the_content', 'descContainer', 'content']})
    return description


def get_image(html):
    """Scrape share image."""
    image = None
    if html.find("meta", property="image"):
        image = html.find("meta", property="image").get('content')
    elif html.find("meta", property="og:image"):
        image = html.find("meta", property="og:image").get('content')
    elif html.find("meta", property="twitter:image"):
        image = html.find("meta", property="twitter:image").get('content')
    elif html.find("img", src=True):
        image = html.find_all("img").get('src')
    return image


def get_site_name(html, url):
    """Scrape site name."""
    if html.find("meta", property="og:site_name"):
        site_name = html.find("meta", property="og:site_name").get('content')
    elif html.find("meta", property='twitter:title'):
        site_name = html.find("meta", property="twitter:title").get('content')
    else:
        site_name = url.split('//')[1]
        return site_name.split('/')[0].rsplit('.')[1].capitalize()
    return site_name


def get_favicon(html, url):
    """Scrape favicon."""
    if html.find("link", attrs={"rel": "icon"}):
        favicon = html.find("link", attrs={"rel": "icon"}).get('href')
    elif html.find("link", attrs={"rel": "shortcut icon"}):
        favicon = html.find("link", attrs={"rel": "shortcut icon"}).get('href')
    else:
        favicon = f'{url.rstrip("/")}/favicon.ico'
    return favicon


def get_theme_color(html):
    """Scrape brand color."""
    if html.find("meta", property="theme-color"):
        color = html.find("meta", property="theme-color").get('content')
        return color
    return None
