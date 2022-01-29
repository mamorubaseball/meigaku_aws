from django.shortcuts import render,redirect
from django.views.generic.base import TemplateView,View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import (CreateView,UpdateView,DeleteView,FormView,)
from .forms import CircleRegistForm,CircleLoginForm,CircleContentUpdateForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages
from .models import CircleContents,Circles
from articles.models import Posts
from django.views.decorators.csrf import requires_csrf_token
from django.http import HttpResponseServerError

@requires_csrf_token
def my_customized_server_error(request, template_name='500.html'):
    import sys
    from django.views import debug
    error_html = debug.technical_500_response(request, *sys.exc_info()).content
    return HttpResponseServerError(error_html)

class HomeView(ListView):
    template_name = 'home.html'
    model = CircleContents
    # queryset = CircleContents.objects.all.order_by('-id')[0:4]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['CircleContents_lists'] = CircleContents.objects.all().order_by('-id')[0:4]
        context['Post_lists']=Posts.objects.all().order_by('-id')[0:4]
        return context


# class IndexView(TemplateView):
#     template_name = 'home'


class CircleRegist(CreateView):
    template_name = 'circle_regist.html'
    form_class = CircleRegistForm

class CircleDetailView(DetailView):
    model = CircleContents
    template_name ='circle_detail.html'
    queryset = CircleContents.objects.order_by('-id')
    def get(self, request, *args, **kwargs):
        circle=CircleContents.objects.get(id=self.kwargs['pk'])
        return render(request,'circle_detail.html',{
            'circle':circle,})


class CircleDelte(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        user = Circles.objects.get(id=self.kwargs['pk'])
        return render(request,'circle_delete.html',{
            'user':user
        })
    def post(self, request, *args, **kwargs):
        circle = Circles.objects.get(id=self.kwargs['pk'])
        circle.delete()
        return redirect('circle_accounts:home')

class CircleLoginView(FormView):
    template_name = 'circle_login.html'
    form_class = CircleLoginForm

    def post(self, request, *args, **kwargs):
        username=request.POST['username']
        password=request.POST['password']
        form=self.get_form()
        print(username)
        print(password)
        circle=authenticate(password=password,username=username)
        print(circle)
        if circle is not None and circle.is_active:
            print('ログイン成功')
            login(request,circle)
        else:
            return self.form_invalid(form)
        return redirect('circle_accounts:circle_login_home',circle.id)

    def form_invalid(self, form):
        messages.error(self.request,'サークル名とパスワードが異なります')
        return super().form_invalid(form)

class CircleLogoutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect('circle_accounts:circle_login')

class CircleHomeView(LoginRequiredMixin,CreateView):
    template_name = 'circle_login_home.html'
    form_class = CircleContentUpdateForm
    success_url = 'circle_accounts:circle_login_home'
    def post(self, request, *args, **kwargs):
        form=CircleContentUpdateForm(request.POST,request.FILES)
        if form.is_valid():
            form.save(commit=False)
            post_data=CircleContents()
            post_data.contents=form.cleaned_data['contents']
            post_data.username_id = request.user.id
            post_data.money=form.cleaned_data['money']
            post_data.place=form.cleaned_data['place']
            post_data.event=form.cleaned_data['event']
            post_data.how_often=form.cleaned_data['how_often']
            post_data.how_often_drink=form.cleaned_data['how_often_drink']
            post_data.member=form.cleaned_data['member']
            post_data.twitter_url=form.cleaned_data['twitter_url']
            post_data.instagram_url=form.cleaned_data['instagram_url']
            post_data.picture=form.cleaned_data['picture']
            post_data.save()

        return redirect('circle_accounts:circle_login_home',self.request.user.id)


    def get(self, request, *args, **kwargs):
        # content = CircleContents.objects.get(id=self.kwargs['pk'])
        form=CircleContentUpdateForm()
        try:
            content = CircleContents.objects.get(username_id=self.request.user.id)
        except:
            content=None
            import traceback
            traceback.print_exc()
            print('=====エラー内容======')

        print(content)
        return render(request, 'circle_login_home.html', {
            'content': content,
            'form': form,
        })


class CircleEditView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        # content = CircleContents.objects.get(id=self.kwargs['pk'])
        # print(self.request.user.id)
        try:
            content = CircleContents.objects.get(username_id=self.request.user.id)
        except:
            content=None

        if content:
            form=CircleContentUpdateForm(
                request.POST or None,
                initial={
                    'contents':content.contents,
                    'how_often':content.how_often,
                    'event':content.event,
                    'place':content.place,
                    'money':content.money,
                    'member':content.member,
                    'how_often_drink':content.how_often_drink,
                    'twitter_url':content.twitter_url,
                    'instagram_url':content.instagram_url,
                    'picture':content.picture,
                }
            )
        else:form=CircleContentUpdateForm()
        return render(request, 'circle_edit.html', {
            'form':form,
        })

    def post(self, request, *args, **kwargs):
        form = CircleContentUpdateForm(request.POST,request.FILES)
        try:
            content_data = CircleContents.objects.get(username_id=self.request.user.id)
        except:content_data=None

        # print(content_data)
        # print('写真データ保存',form.cleaned_data['picture'])

        if form.is_valid():
            print('フォームok')
            post_data=CircleContents(username_id=self.request.user.id)
            post_data.contents=form.cleaned_data['contents']
            post_data.username_id=request.user.id
            post_data.money=form.cleaned_data['money']
            post_data.place=form.cleaned_data['place']
            post_data.event=form.cleaned_data['event']
            post_data.how_often=form.cleaned_data['how_often']
            post_data.how_often_drink=form.cleaned_data['how_often_drink']
            post_data.member=form.cleaned_data['member']
            post_data.twitter_url=form.cleaned_data['twitter_url']
            post_data.instagram_url=form.cleaned_data['instagram_url']
            post_data.picture=form.cleaned_data['picture']
            if content_data:
                content_data.delete()
            post_data.save()
            print('フォームok')
            return redirect('circle_accounts:circle_login_home',self.request.user.id)







