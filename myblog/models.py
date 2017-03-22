# -*- coding:utf8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib import admin
from django.core.urlresolvers import reverse


class BlogBody(models.Model):
    blog_title = models.CharField(max_length=100, verbose_name=u'标题')
    blog_tags = models.CharField(max_length=200, null=True, blank=True, help_text=u'用逗号分隔')
    blog_abstract = models.TextField(verbose_name=u'摘要')
    blog_body = models.TextField(verbose_name=u'正文')
    blog_type = models.CharField(max_length=50)
    blog_timestamp = models.DateTimeField(u'创建时间')
    blog_update_time = models.DateTimeField(u'更新时间')
    blog_imgurl = models.CharField(max_length=50, null=True)
    blog_author = models.CharField(max_length=20, verbose_name=u'作者')
    blog_ismarkdown = models.CharField(max_length=1, null=True)
    blog_like = models.IntegerField(default=0)
    blog_clicknum = models.IntegerField(default=0)
    blog_is_top = models.BooleanField(default=False, verbose_name=u'置顶')

    def __unicode__(self):
        return self.blog_title

    def get_tags(self):
        tags_list = self.blog_tags.split(',')
        while '' in tags_list:
            tags_list.remove('')
        return tags_list

    def get_absolute_url(self):
        return reverse('article', args=(self.id,))


class UserInfo(models.Model):
    nickname = models.CharField(max_length=20)
    work = models.CharField(max_length=20)
    company = models.CharField(max_length=50)
    email = models.CharField(max_length=20)

    def __unicode__(self):
        return self.nickname

admin.site.register(BlogBody)
admin.site.register(UserInfo)
