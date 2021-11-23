from googlesearch import search
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect


def serpapiView(request):
    # print("No module named 'google' found")
    title = 'Google Search'
    if request.method == "POST":
        # to search
        search_keyword = request.POST.get('search_keyword', None)
        query = search_keyword

        for j in search(query, tld="co.in", num=10, stop=10, pause=2):
            print(j)

    context = {
        'title': title
    }
    return render(request, 'admin/serpapi/search.html', context)
