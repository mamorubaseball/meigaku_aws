from django.db import models
from django.conf import settings
from django.utils import timezone
from circle_accounts.models import Circles
from django.contrib.auth.models import (
User,BaseUserManager,AbstractBaseUser,PermissionsMixin
)

# class UsersManager(BaseUserManager):
#     def create_superuser(self,username,email,password=None):
#         user=self.model(
#             username=username,
#             email=email,
#         )
#         user.set_password(password)
#         user.is_staff=True
#         user.is_active=True
#         user.is_superuser=True
#         user.save(using=self._db)
#         return user
#
# class Users(AbstractBaseUser,PermissionsMixin):
#     username =models.CharField('ユーザー名',max_length=190,unique=True)
#     email = models.EmailField('メール', max_length=200)
#     is_active = models.BooleanField(default=True)
#     is_staff=models.BooleanField(default=False)
#     USERNAME_FIELD = 'username'
#     # スーあーユーザーを作成する際に必要なもの。
#     REQUIRED_FIELDS = ['email']
#     objects = UsersManager()


class Posts(models.Model):
    username = models.ForeignKey(
        Circles,on_delete=models.CASCADE
    )
    picture=models.FileField(upload_to='user/',null=True)
    title = models.CharField(max_length=200,null=True)
    title_url=models.URLField(max_length=200,null=True)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    category = models.CharField(max_length=200,default='学生生活')

    def __str__(self):
        return self.title
#
# class Like(models.Model):
#     article = models.ForeignKey(Posts, on_delete=models.CASCADE)
#     timestamp = models.DateTimeField(default=timezone.now)


