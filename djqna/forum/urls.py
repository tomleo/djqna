from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^questions/$', views.questions, name='questions'),
    url(r'^question/(?P<question_id>[0-9]+)/$', views.question, name='question'),
    url(r'^answers/(?P<question_id>[0-9]+)/$', views.answers, name='answers'),
    url(r'^answer/(?P<answer_id>[0-9]+)/$', views.answer, name='answer'),
]

