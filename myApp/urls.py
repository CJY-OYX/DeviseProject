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
]