"""RealtimeBridge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from server import views, auth
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^event/$', views.event, name='event'),
    url(r'^login/', auth.login, name='login'),
    url(r'^logout/', auth.logout, name='logout'),
    url(r'^condition/', views.condition),

    url(r'^bridges/$', views.BridgeList.as_view(), name='bridge_list'),
    url(r'^bridges/(?P<pk>[0-9]+)/$', views.BridgeDetail.as_view(), name='bridge_detail'),
    url(r'^bridges/create/$', views.BridgeCreate.as_view(), name='bridge_create'),
    url(r'^bridges/update/(?P<pk>[0-9]+)/$', views.BridgeUpdate.as_view(), name='bridge_update'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
