from django.urls import path
from . import views, adminView, scrapView, serpapi
from .adminView import SemrushUploadView, SemrushList, SemrushListDelete, SemrushDatatablesView
from .googleSearchView import SemrushGetLinks, SerpListUpload, GoogleList, LinksDatataleView, GoogleLinksAjax
from .scrapView import ScrapList, scrap_list_json, scrapDataView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Frontend Path
    path('', views.home_frontend, name='frontend'),

    # Backend Path
    path('admin', adminView.backend_home),
    path('admin/user-pending', adminView.user_pending, name='user_pending'),

    # Authentication
    # path(r'^login/$', RedirectView.as_view(pattern_name='login', permanent=False)),
    path('login', adminView.backend_login, name='login'),
    path('password', adminView.forget_password, name='forgot-password'),
    path('admin/logout', adminView.user_logout, name='logout'),
    path('admin/register', adminView.user_Register, name='register'),


    #Semrush Upload CSV file
    path('admin/semrush', SemrushList.as_view(), name='semrush'),
    path('admin/semrushAjax', SemrushDatatablesView.as_view(), name='list_json'),
    path('admin/semrush/add', SemrushUploadView.as_view(), name='semrush_add'),
    path('admin/semrush/delete/<int:pk>', SemrushListDelete, name='semrush_delete'),
    path('admin/semrush/<str:keyword>/<int:pk>', SemrushGetLinks.as_view(), name='get_links'),

    # GetLinks on google Links
    path('admin/google_links', SerpListUpload.as_view(), name='google_list'),
    path('admin/google/linkAjax', LinksDatataleView.as_view(), name='google_links_ajx'),
    path('admin/google/links', GoogleList.as_view(), name='list_links'),
    path('admin/google/uploadLinkAjax', GoogleLinksAjax.as_view(), name='bulk_link_upload'),

    # scraping Data View
    path('admin/scrap/list', ScrapList.as_view(), name='scrap_view'),
    path('admin/scrap/listAjax', scrap_list_json.as_view(), name='scrap_list_json'),
    path('admin/scrap/view/<int:pk>', scrapDataView.as_view(), name='scrap_links'),

    #bs4 Scrapping
    path('admin/serapi/search', serpapi.serpapiView, name="search_api"),
    path('admin/scrap/add', scrapView.djbs, name="add_scrap"),

]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)