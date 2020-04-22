from django.conf.urls import url
from . import views

app_name = 'gestionArticulos'

urlpatterns = [
    url(r'^resultados/$', views.articles_results, name='artresults'),
    url(r'^articulo/$', views.article, name='art')
]