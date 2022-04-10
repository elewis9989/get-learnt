from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^listings/$', views.listings, name='listings'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^detail/(?P<skill_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^create-listing/$', views.createListings, name='createListing'),
    url(r'^create-review/(?P<user_id>[0-9]+)/(?P<listing_id>[0-9]+)/$', views.CreateReview, name='CreateReview'),
    url(r'^search/$', views.search, name='search')

] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
