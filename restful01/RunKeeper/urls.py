from django.conf.urls import url
from . import views


urlpatterns = [



    url(r'^sessions/$',
        views.SessionList.as_view(),
        name=views.SessionList.name),

    url(r'^sessions/(?P<pk>[0-9]+)$',
        views.SessionSpecificSpeed.as_view(),
        name=views.SessionSpecificSpeed.name),

    url(r'^sessions/totaldistance',
        views.TotalDistance.as_view(),
        name=views.TotalDistance.name
        ),


    url(r'^sessions/averagespeed',
        views.AverageSpeed.as_view(),
        name=views.AverageSpeed.name
        ),

    url(r'^sessions/login',
        views.LoginView.as_view(),
        name=views.LoginView.name
        ),

    url(r'^sessions/logout',
        views.LogoutView.as_view(),
        name=views.LoginView.name
        ),

    url('',
        views.ApiRoot.as_view(),
        name=views.ApiRoot.name),
]

# url(r'^$',
# views.ApiRoot.as_view(),
# name=views.ApiRoot.name),
