from django.conf.urls import url
from . import views

app_name = 'gestionArticulos'

urlpatterns = [
    url(r'^resultados/$', views.articles_results, name='artresults'),
    url(r'^articulo/$', views.article, name='art'),
    url(r'^registrararticulo/$', views.add_article, name='add_article'),
    url(r'^misarticulos/$', views.my_articles, name='my_articles'),    
]