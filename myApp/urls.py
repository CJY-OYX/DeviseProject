from django.urls import path
from myApp import views
urlpatterns = [
    path("register/", views.register, name="register"),
    path("center/", views.center,name="center"),
    path("centerLeft/", views.centerLeft,name="centerLeft"),
    path("bottomLeft/", views.bottomLeft,name="bottomLeft"),
    path("centerRight/", views.centerRight,name="centerRight"),
    path("centerRightChange/<int:energyType>", views.centerRightChange,name="centerRightChange"),
    path("bottomRight/", views.bottomRight,name="bottomRight"),
    path("search-cars/", views.search_cars, name="search_cars"),
    path("save-user-car-detail/", views.save_user_car_detail, name="save_user_car_detail"),
    path("entry-user-info/",views.entry_user_info,name='entry_user_info'),
    path("login/",views.login,name='login'),
    path("get-user-info/", views.get_user_info, name="get_user_info"),
    path("get-car-info/", views.get_car_info, name="get_car_info"),
    path("get-user-car-detail/", views.get_user_car_detail, name="get_user_car_detail"),
    path("if-user-car-detail/", views.if_user_car_detail, name="if_user_car_detail"),
]