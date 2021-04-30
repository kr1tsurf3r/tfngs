from django.urls import path

#from . import views
from .views import MatchListView

urlpatterns = [
    #path('', views.index, name='index'),
    path('', MatchListView.as_view(), name = "index")
]

