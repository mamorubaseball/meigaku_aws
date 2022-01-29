from django.urls import path,include
from .views import NewPostView,PostListView,PostDetailView

app_name='articles'
urlpatterns = [
    path('', NewPostView.as_view(), name='new_post'),
    path('post_detail/<int:pk>', PostDetailView.as_view(), name='post_detail'),
]