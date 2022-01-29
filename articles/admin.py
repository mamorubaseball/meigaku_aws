from django.contrib import admin
from .models import Posts
from .forms import PostContentForm

# class PostAdmin(admin.ModelAdmin):
#
#     #textareaを表示させるフォームクラスを指定。
#     form = PostContentForm

admin.site.register(Posts)
# admin.site.register(Like)