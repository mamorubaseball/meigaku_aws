from django.urls import path
from .views import HomeView,\
    CircleLoginView,CircleRegist,CircleHomeView,\
    CircleLogoutView,CircleEditView,CircleDelte,\
    CircleDetailView
from articles.views import PostListView,PostDetailView
from django.contrib import admin

app_name='circle_accounts'

urlpatterns=[
    # path('home/',BaseView.as_view(),name='base'),
    path('home/',HomeView.as_view(),name='home'),
    path('circle_regist/',CircleRegist.as_view(),name='circle_regist'),
    path('circle_login/',CircleLoginView.as_view(),name='circle_login'),
    path('circle_logout/',CircleLogoutView.as_view(),name='circle_logout'),
    path('circle_login_home/<int:pk>',CircleHomeView.as_view(),name='circle_login_home'),
    path('circle_edit/<int:pk>',CircleEditView.as_view(),name='circle_edit'),
    path('circle_delete/<int:pk>',CircleDelte.as_view(),name='circle_delete'),
    path('circle_detail/<int:pk>',CircleDetailView.as_view(),name='circle_detail'),
]