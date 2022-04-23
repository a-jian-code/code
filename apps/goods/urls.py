from django.urls import path, re_path
from goods.views import IndexView, DetailView,ListView
from apps.goods import views

urlpatterns = [
    path('index/',IndexView.as_view(),name='index') , #首页
    re_path(r'^detail/(\d+)/$', DetailView.as_view(), name='detail'), # 详情页
    re_path(r'^list/(\d+)/(\d+)/$',  ListView.as_view(), name='list'), # 列表页
    path('',IndexView.as_view(),name='index') , #首页
]
