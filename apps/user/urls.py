from django.urls import path,re_path
from user.views import RegisterView,ActiveView,LoginView,LogoutView,UserInfoView, UserOrderView, AddressView

urlpatterns = [
    # path('register/',views.register, name='register'),  #注册
    # path('register_handle/',views.register_handle, name='register_handle') #注册处理
    path('register',RegisterView.as_view(), name='register'),
    re_path('active/(?P<token>.*)/',ActiveView.as_view(),name='active'), #用户激活
    path('login/',LoginView.as_view(),name='login') , #用户登录
    path('logout/',LogoutView.as_view(),name='logout') , #用户登录

    path('', UserInfoView.as_view(),name='user'),# 用户中心信息页
    re_path(r'^order/(\d*)/$',UserOrderView.as_view(),name='order'),#用户中心订单页
    path('address/',AddressView.as_view(),name='address'),#用户中心地址页
]
