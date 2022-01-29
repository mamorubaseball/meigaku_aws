from django.db import models
from django.contrib.auth.models import (
User,BaseUserManager,AbstractBaseUser,PermissionsMixin
)
from django.urls import reverse_lazy


class CirclesManager(BaseUserManager):
    def create_user(self,username,email,password=None):
        if not email:
            raise ValueError('メール入力必須')

        user=self.model(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    #スーパーユーザーだけが記事投稿できる仕組み。また、サークル記事の編集もスーパーユーザには権限がある。
    def create_superuser(self,username,email,password=None):
        user=self.model(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.is_staff=True
        user.is_active=True
        user.is_superuser=True
        user.save(using=self._db)
        return user


class Circles(AbstractBaseUser,PermissionsMixin
              ):
    username=models.CharField('サークル名',max_length=190,unique=True)
    email=models.EmailField('メール',max_length=200)
    # password=models.CharField('パスワード',max_length=190,unique=True)
    is_active = models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)

    #このレコードを一意に識別するためのものこれでログインする
    USERNAME_FIELD='username'
    #スーあーユーザーを作成する際に必要なもの。
    REQUIRED_FIELDS = ['email']
    objects = CirclesManager()

    def get_absolute_url(self):
        return reverse_lazy('circle_accounts:circle_login')

class CircleContents(models.Model):
    username = models.ForeignKey(
        Circles,on_delete=models.CASCADE,
    )

    CHOICES = [
        ('0', 0),
        ('1', 1),
        ('2', 2),
        ('3', 3),
        ('4', 4),
        ('5', 5),
    ]
    contents=models.TextField('活動内容',max_length=1000)
    how_often=models.CharField('活動頻度(週に何回活動しますか？)',choices=CHOICES,blank=True,max_length=100)
    event=models.CharField('イベント',max_length=1000)
    place=models.CharField('活動場所',max_length=1000)
    money=models.CharField('活動費用',max_length=1000)
    member=models.IntegerField('所属人数')
    how_often_drink=models.CharField('飲み会の頻度(週に何回)',choices=CHOICES,blank=True,max_length=100)
    twitter_url=models.URLField(blank=True)
    instagram_url=models.URLField(blank=True)
    picture=models.FileField(upload_to='circle_pictures/')

