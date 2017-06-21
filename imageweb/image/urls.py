from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    url(r'^$', views.image, name='image'),
    url(r'(?P<article_id>[0-9]+)/$', views.article_page, name='article_page'),
    url(r'(?P<article_id>[0-9]+)/comment/$', views.comment, name='comment'),
    url(r'(?P<article_id>[0-9]+)/keep/', views.keep, name='keep'),
    url(r'(?P<article_id>[0-9]+)/poll/', views.poll, name='poll'),
    url(r'post/$', views.post, name='post'),
    url(r'post/postimage/', views.post_image, name='post_image'),
    url(r'^search/', include('haystack.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)