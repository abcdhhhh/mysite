from django.urls import path
from django.conf.urls import include
from django.contrib import admin
from login import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('ask/', views.ask),
    path('question/<int:qid>/', views.question),
    path('delquestion/<int:qid>/', views.delquestion),
    path('question/<int:qid>/answer/', views.answer),
    path('question/<int:qid>/delanswer/<int:aid>/', views.delanswer),
    path('questionlist/', views.questionlist),
    path('questionlist/search/', views.search),
    path('ranking/', views.ranking),
    path('about/', views.about),
    path('login/', views.login),
    path('register/', views.register),
    path('findback/', views.findback),
    path('logout/', views.logout)
]
