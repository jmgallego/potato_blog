from django.conf.urls import patterns, include, url
from django.contrib import admin
import dbindexer

handler500 = 'djangotoolbox.errorviews.server_error'

# django admin
admin.autodiscover()

# search for dbindexes.py in all INSTALLED_APPS and load them
dbindexer.autodiscover()

urlpatterns = patterns('',
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    ('^admin/', include(admin.site.urls)),
    (r'^logout/$', 'django.contrib.auth.views.logout',{'next_page':'/'}),
    url('^$','my_blog.views.home',name="home"),
    url('^do_article/$','my_blog.views.do_article',name="do_article"),
    url('^pull_articles/$','my_blog.views.pull_articles',name="pull_articles"),
    url('^get_article/$','my_blog.views.get_article',name="get_article"),
    url('^delete_article/$','my_blog.views.delete_article',name="delete_article"),
)
