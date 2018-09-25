
from django.conf.urls import url

from front import views

urlpatterns = [
    url(r'^index/', views.index, name='index'),
    url(r'^article/(\d+)/', views.article, name='article'),
    url(r'^about/', views.about, name='about'),
    url(r'^index2/', views.index2, name='index2'),
]
