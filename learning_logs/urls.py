''' learning_logs URL 패턴 정의 '''

from django.conf.urls import url, include
from . import views

urlpatterns = [
    # 홈페이지
    url(r'^$', views.index, name='index'),
    # 주제표시?
    url(r'^topics/$', views.topics, name='topics'),
    # 주제 하나에 대한 세부사항 페이지
    #url(r'^topics/(?P<topic_id>\d+)/$', views.topic, name='topic'),
    url(r'^topics/(?P<topic_id>[0-9]+)/$', views.topic, name='topic'),
    url(r'^new_topic/$', views.new_topic, name='new_topic'),
    url(r'^new_entry/(?P<topic_id>\d+)/$', views.new_entry, name='new_entry'),
    url(r'^edit_entry/(?P<entry_id>\d+)/$', views.edit_entry, name='edit_entry'),

    url(r'^edit_entry/(?P<topic_id>\d+)/delete/(?P<entry_id>\d+)/$', views.entry_delete, name='entry_delete'),

    
    url(r'^topics/(?P<topic_id>[0-9]+)/comment$', views.add_comment_to_post, name='add_comment_to_post'),
]
#</topic_id>
