from django.urls import path
from . import views, adminView, scrapView, serpapi, googleSearchView, adminpanelView, jsonView
from .adminView import SemrushUploadView, SemrushList, SemrushListDelete, SemrushDatatablesView
from .googleSearchView import SemrushGetLinks, SerpListUpload, GoogleList, LinksDatataleView, GoogleLinksAjax, GoogleLinksDelete
from .scrapView import ScrapList, scrap_list_json, scrapDataView, ScrapListDelete, ScrapData
from .jsonView import googleAPI, JsonDataView, JsonDataList, PermissionAjaxDatatableView, JsonListDelete
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Frontend Path
    path('', views.home_frontend, name='frontend'),

    # Backend Path
    path('admin/', adminView.backend_home),
    path('admin/user-pending', adminView.user_pending, name='user_pending'),

    # Admin Panel View
    path('admin/user/', adminpanelView.AdminUserList, name='user_list'),
    # path('admin/auth/user/delete/<int:pk>', adminpanelView.AdminUserDelete, name='auth_user_delete'),
    path('admin/user/<int:id>/edit/',
         adminpanelView.AdminUserEdit, name='user_view'),
    path('admin/user/<int:id>/view/',
         adminpanelView.AdimUserView, name="user_display"),


    # Authentication
    path('admin/', adminView.RedirectView, name='admin'),
    path('admin/login/', adminView.backend_login, name='login'),
    path('password', adminView.forget_password, name='forgot-password'),
    path('admin/logout', adminView.user_logout, name='logout'),
    path('admin/register', adminView.user_Register, name='register'),


    # Semrush Upload CSV file
    path('admin/semrush', SemrushList.as_view(), name='semrush'),
    path('admin/semrushAjax', SemrushDatatablesView.as_view(), name='list_json'),
    path('admin/semrush/add', SemrushUploadView.as_view(), name='semrush_add'),
    path('admin/semrush/delete/<int:pk>',
         SemrushListDelete, name='semrush_delete'),
    path('admin/semrush/<str:keyword>/<int:pk>',
         SemrushGetLinks.as_view(), name='get_links'),

    # GetLinks on google Links
    path('admin/google_links', SerpListUpload.as_view(), name='google_list'),
    path('admin/google/linkAjax', LinksDatataleView.as_view(),
         name='google_links_ajx'),
    path('admin/google/links', GoogleList.as_view(), name='list_links'),
    path('admin/google/uploadLinkAjax',
         GoogleLinksAjax.as_view(), name='bulk_link_upload'),
    path('admin/google/delete/<int:pk>',
         GoogleLinksDelete, name='googlelink_delete'),

    # scraping Data View
    path('admin/scrap/list', ScrapList.as_view(), name='scrap_view'),
    path('admin/scrap/listAjax', scrap_list_json.as_view(), name='scrap_list_json'),
    path('admin/scrap/view/<int:pk>', scrapDataView.as_view(), name='scrap_links'),
    path('admin/scrap/delete/<int:pk>',
         ScrapListDelete, name='scrap_list_delete'),

    # bs4 Scrapping
    path('admin/serapi/search', serpapi.serpapiView, name="search_api"),
    path('admin/scrap/add', scrapView.djbs, name="add_scrap"),



    # Scrap Data URL
    path('admin/scrap/data', ScrapData.as_view(), name="scrap_data"),

    # json data view URL
    path('admin/scrap/json', jsonView.JsonDataView, name="json_data_view"),
    path('admin/scrap/json/save', jsonView.JsonDataSave, name="json_data_store"),
    path('admin/scrap/json/list', JsonDataList.as_view(), name="json_data_list"),
    path('ajax_datatable/permissions/', PermissionAjaxDatatableView.as_view(),
         name="ajax_datatable_permissions"),
    path('admin/scrap/json/delete/<int:pk>',
         JsonListDelete, name='json_delete'),


    # google api for json data
    path('admin/scrap/google/json', jsonView.googleAPI, name="google_api_view"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
