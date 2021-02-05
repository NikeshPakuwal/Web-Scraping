from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Semrush, UploadGoogleDataLink, ScrapGoogleDataLinkData
from datatables_view.views import DatatablesView
from django.urls import reverse_lazy
from django.views import View
from googlesearch import search
from bs4 import BeautifulSoup
import requests
from django.contrib import messages


@method_decorator(login_required, name='dispatch')
class SemrushGetLinks(View):
    login_url = 'backend/login'

    def get(self, request, keyword, pk):
        title = 'Google Links Upload'
        query = keyword

        search_keyword = search(query, tld="co.in", num=10, stop=10, pause=2)
        list_keyword=[]
        for row in search_keyword:
            list_keyword.append(row)

        all_links = UploadGoogleDataLink.objects.all()

        links = []
        for link_rows in all_links:
            links.append(link_rows.links)

        context = {
            'title': title,
            'list': list_keyword,
            'id': pk,
            'all_links': links,
            'message': messages.success(request, 'Your Google Data here')
        }

        return render(request, 'admin/serpapi/search.html', context)

@method_decorator(login_required, name='dispatch')
class SerpListUpload(View):
    login_url = 'backend/login'
    def post(self, request):
        get_links = request.POST.getlist('links')
        keyword_id = request.POST.get('keyword_id')

        list_of_list = list(get_links)
        objs = [
            UploadGoogleDataLink(
                links=row,
               keyword_id_id=keyword_id
            )
            for row in list_of_list
        ]
        try:
            msg = UploadGoogleDataLink.objects.bulk_create(objs)
            context = {
                'message': messages.success(request, 'Your Google Data has been successfully uploaded.')
            }
        except Exception as e:
            context = {
                'message': messages.error(request, 'Your Google Data has been successfully uploaded.')
            }

        return render(request, 'admin/serpapi/list.html', context)


class GoogleList(View):

    def get(self, request):
        title = 'Google Data List'
        context = {
            'title': title,
        }
        template_name = 'admin/serpapi/list.html'
        return render(request, template_name, context)

class GoogleLinksAjax(View):


    def post(self, request):
        URL = "http://api.proxiesapi.com"

        auth_key = "8aaf4535c3d7b6e0efd39ffe898f6efa_sr98766_ooPq87"
        session = "444"

        ids = request.POST.getlist('id[]')

        new_arr = []
        for row in ids:
            google_info = UploadGoogleDataLink.objects.get(id=row)
            links = google_info.links

            page_url = links

            PARAMS = {'auth_key': auth_key, 'url': page_url, 'render': 'true'}

            r = requests.get(url=URL, params=PARAMS)

            html = BeautifulSoup(r.content, 'html.parser')

            new_arr.append(
                ScrapGoogleDataLinkData(
                    keyword_id=row,
                    title= self.get_title(html),
                    content= str(self.get_description(html))
                )
            )

        ScrapGoogleDataLinkData.objects.bulk_create(new_arr)
        return HttpResponse(new_arr)
        # try:
        #     msg = ScrapGoogleDataLinkData.objects.bulk_create(new_arr)
        #     returnmsg = {"status_code": 200}
        # except Exception as e:
        #     print('Error While Importing Data: ', e)
        #     returnmsg = {"status_code": 500}
        #
        # return JsonResponse(returnmsg)

        # return render(request, 'admin/scraping/django-bs.html', {'result': new_arr})

    def get_title(self,html):
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

    def get_description(self,html):
        """Scrape page description."""
        description = None
        if html.find("article"):
            description = html.find("article")
        elif html.find("div", {
            'class': ['wrap-content-main', 'post_the_content', 'mw-parser-output', 'descContainer', 'content']}):
            description = html.find(True, {
                'class': ['wrap-content-main', 'mw-parser-output', 'post_the_content', 'descContainer', 'content']})
        elif html.find("main", id_='main'):
            description = html.find("main")
        elif html.find("p"):
            description = html.body.find_all('p')

        # description = html.find(True, {'class':['wrap-content-main', 'post_the_content', 'descContainer', 'content']})
        return description

    def get(self, request):
        title = 'Google Data List'
        context = {
            'title': title,
        }
        template_name = 'admin/serpapi/list.html'
        return render(request, template_name, context)

@method_decorator(login_required, name='dispatch')
class LinksDatataleView(DatatablesView):
    model = UploadGoogleDataLink
    column_defs = [
        {
            'name': 'sn',
            'title': 'sn',
            'className': 'checkbox_input',
            'defaultContent': '<h1>test</h1>',
            'searchable': True,
            'orderable': False,
        },{
            'name': 'id',

        }, {
            'name': 'keyword_id',
            'foreign_field': 'keyword_id__keyword',

        }, {
            'name': 'links',
            'searchable': False
        },
        {
            'name': 'Action',
            'searchable': False
        }
    ]

    def customize_row(self, row, obj):
        row['sn'] = '<input type="checkbox" name="chk_list" class="checklist" data-cid="%s" id="chk_%s">' % (
        obj.id, obj.id)
        # row['Action'] = '<a href="/%s" class="btn btn-primary"><i class="fas fa-pen"></i></a>' % obj.id
        row['Action'] = '<a data-url="%s" class="btn btn-danger delete_button">%s</a>' % (
            reverse_lazy('semrush_delete', args=(obj.id,)),
            '<i class="fas fa-trash-alt"></i>'
        )

        return
