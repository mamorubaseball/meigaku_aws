from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .forms import PostContentForm
from .models import Posts
from django.shortcuts import render,redirect

class NewPostView(LoginRequiredMixin,CreateView):
    pass

class PostListView(ListView):
    template_name = 'home.html'
    model = Posts
    post_lists = Posts.objects.order_by('-id')
    liked_lists=[]

    # for post in post_lists:
    #     liked=post.like_set()
    #     if liked.exsits():
    #         liked_lists.append(post.id)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['post_lists'] = Posts.objects.all
        # context['liked_lists']= liked_lists
        return context

class PostDetailView(DetailView):
    model = Posts
    template_name ='post_detail.html'
    queryset = Posts.objects.order_by('-id')
    def get(self, request, *args, **kwargs):
        post=Posts.objects.get(id=self.kwargs['pk'])
        return render(request,'post_detail.html',{
            'post':post })

