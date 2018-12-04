from django.conf.urls import url
from django.views.generic import TemplateView
from ncloud.views_ai_app import *
from ncloud.views_iaas import *
from ncloud.views import *
from ncloud.API_List import *

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

urlpatterns = [

    url(r'^api/$', index, name='index'),

    # AI / Application
    url(r'^CSS$', CSS, name='CSS'),
    url(r'^nShortURLTest$', nShortURLTest, name='nShortURLTest'),
    url(r'^mapsTest$', mapsTest, name='mapsTest'),

    url(r'^api/ai_clova$', Clova, name='Clova'),
    url(r'^api/Maps$', Maps, name='Maps'),
    url(r'^api/Papago$', Papago, name='Papago'),
    url(r'^api/nShortURL$', nShortURL, name='nShortURL'),
    url(r'^api/CAPTCHA$', CAPTCHA, name='CAPTCHA'),
    url(r'^api/CAPTCHA_Check$', CAPTCHA_Check, name='CAPTCHA_Check'),
    url(r'^api/SearchTrend$', SearchTrend, name='SearchTrend'),
    url(r'^api/APIGW/$', APIGW, name='APIGW'),

    # PasS
    url(r'^api/geoLocation/$', geoLocation, name='geoLocation'),

    # IaaS
    url(r'^api/(?P<category>[a-z]+)/(?P<service>[a-zA-Z]+)/$', ServiceUrl, name='ServiceUrl'),
    url(r'^api/IaaS$', IaaS, name='IaaS'),

    # URL List
    url(r'^api/IaaS_API$', IaaS_API, name='IaaS_API'),
    url(r'^api/PaaS_API$', PaaS_API, name='PaaS_API'),
    url(r'^api/App_API$', App_API, name='App_API'),

]
