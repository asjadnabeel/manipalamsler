from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^patient/$', views.PatientListView.as_view(), name='patient'),
    url(r'^patient/(?P<pk>\d+)$', views.PatientDetailView.as_view(), name='patient-detail'),
    url(r'^about/$', views.about, name = 'about'),
    url(r'^patient/(?P<pk>\d+)/(?P<uid>[0-9A-Za-z-]+)/$', views.amsler, name='amsler'),
    url(r'^addpatient/$', views.addpatient, name='addpatient')


]
#    url(r'^about/$', views.about, name = 'about'),
#   url(r'^patient/(?P<pk>\d+)/(?P<uid>[0-9A-Za-z-]+)/$', views.amsler, name='amsler')