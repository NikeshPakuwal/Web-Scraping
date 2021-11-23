from django.http import HttpResponse, JsonResponse
from .forms import JsonDataStore
from django.contrib import messages
from .models import StoreJsonData
from django.shortcuts import redirect

from django.shortcuts import render
import requests
import json
import os

from django.views.generic import View, ListView
from ajax_datatable.views import AjaxDatatableView
from django.urls import reverse_lazy

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# multiple json data view


def JsonDataView(request):
    title = "Json Data View"
    data = ""
    json_file_url = os.path.join(BASE_DIR, 'app/jsonData/')

    query = request.POST.get('select')

    if query is not None and query != '':
        with open(json_file_url + query + '.json', encoding='utf-8') as file:
            data = json.load(file)

    context = {
        'title': title,
        'query': query,
        'data': data
    }
    return render(request, "admin/json/json_view.html", context)


# store checked json data in database
def JsonDataSave(request):
    form = ""
    if request.method == "POST":
        title = request.POST.get('title')
        type = request.POST.get('type')
        images = request.POST.getlist('images []')
        source = request.POST.get('source')
        description = request.POST.get('description')
        born = request.POST.get('born')
        height = request.POST.get('height')
        books = request.POST.getlist('books []')
        education = request.POST.get('education')
        children = request.POST.getlist('children []')
        known_attributes = request.POST.getlist('known_attributes []')
        profiles = request.POST.getlist('profiles []')
        people_also_search_for = request.POST.getlist(
            'people_also_search_for []')
        related_searches = request.POST.getlist('related_searches []')
        related_questions = request.POST.getlist('related_questions []')
        organic_results = request.POST.getlist('organic_results []')
        pagination = request.POST.get('pagination')
        form = StoreJsonData(title=title, type=type, images=images, source=source, description=description, born=born,
                             height=height, books=books, education=education, children=children, known_attributes=known_attributes,
                             profiles=profiles, people_also_search_for=people_also_search_for, related_searches=related_searches,
                             related_questions=related_questions, organic_results=organic_results, pagination=pagination)
        form.save()

    context = {
        'form': form
    }

    return redirect('/admin/scrap/json/list', context)


# json data view from database
class JsonDataList(ListView):

    def get(self, request):
        title = 'Json Data List'
        context = {
            'title': title
        }
        template_name = 'admin/json/jsondata_list.html'
        return render(request, template_name, context)


class PermissionAjaxDatatableView(AjaxDatatableView):
    model = StoreJsonData
    title = 'Json Data List'

    column_defs = [
        {
            'name': 'title',
        },
        {
            'name': 'type',
        },
        {
            'name': 'images',
            'searchable': False,
        },
        {
            'name': 'source',
            'searchable': False,
        },
        {
            'name': 'description',
            'searchable': False,
        },
        {
            'name': 'born',
            'searchable': False,
        },
        {
            'name': 'height',
            'searchable': False,
        },
        {
            'name': 'books',
            'searchable': False,
        },
        {
            'name': 'education',
            'searchable': False,
        },
        {
            'name': 'children',
            'searchable': False,
        },
        {
            'name': 'known_attributes',
            'searchable': False,
        },
        {
            'name': 'profiles',
            'searchable': False,
        },
        {
            'name': 'people_also_search_for',
            'searchable': False,
        },
        {
            'name': 'related_searches',
            'searchable': False,
        },
        {
            'name': 'related_questions',
            'searchable': False,
        },
        {
            'name': 'organic_results',
            'searchable': False,
        },
        {
            'name': 'pagination',
            'searchable': False,
        },
        {
            'name': 'action',
            'searchable': False,
            'orderable': False
        }
    ]

    def customize_row(self, row, obj):
        row['action'] = '<a data-url="%s" class="btn btn-danger delete_button">%s</a>' % (
            reverse_lazy('json_delete', args=(obj.id,)),
            '<i class="fas fa-trash-alt"></i>'
        )
        row['source'] = '%s' % (
            json.dumps(obj.source),
        )


# delete json data from json data list
def JsonListDelete(request, pk):
    data = StoreJsonData.objects.get(id=pk)
    data.delete()
    return redirect(reverse_lazy('json_data_list'))


# google API JSON data
def googleAPI(request):
    title = "Google API"

    keyword = request.POST.get('keyword')

    response = requests.get(
        'https://www.googleapis.com/customsearch/v1?key=AIzaSyDF0hcHyFC9XgCVDG84PROyHBnVm4EQDBM&cx=017576662512468239146:omuauf_lfve&q=' + str(keyword))

    data = response.json()
    keyword_search = json.dumps(data)

    context = {
        'title': title,
        'keyword_search': keyword_search
    }
    # return HttpResponse(keyword_search)

    return render(request, 'admin/scraping/googleAPI_json.html', context)
