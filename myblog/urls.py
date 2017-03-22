from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^article/(\d+)/$', views.article, name='article'),
    url(r'^list/(?P<list_type>\S+)/(?P<page>[0-9]+)/$', views.article_list, name='article_list'),
    url(r'^search/$', views.search_article, name='search'),
    url(r'^weather/$', views.weather, name='weather'),
    url(r'^search_by_tag/(?P<tag>\S+)$', views.search_by_tag, name='search_by_tag'),
    url(r'^liuyan/$', views.liuyan, name='liuyan'),
]
