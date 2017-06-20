from django.conf.urls import url, include
from .views import upload_view, about, HomeView, FolderView, VideoView
from django.views.generic import ListView, DetailView
from watchanime.models import Anime

urlpatterns = [
    #url(r'^$', ListView.as_view(queryset=Anime.objects.all().order_by("-date")[:25],
	#							template_name="watchanime/home.html")),
	url(r'^$', HomeView.as_view()),
	url(r'^about/$', about, name='about'),
	url(r'^upload/$', upload_view.as_view()),
	url(r'^(?P<folderName>[\w().\'!@~ +-\[\]]+)/$', FolderView.as_view()),
	url(r'^(?P<folderName>[\w().\'!@~ +-\[\]]+)/(?P<fileName>[\w().\'!@ ~+-\[\]]+)$', VideoView.as_view()),
	#url(r'^(?P<pk>\d+)$', DetailView.as_view(model=Anime,
	#										 template_name='watchanime/watch.html')),
]
