# -*- coding:utf8 -*-
from django.shortcuts import render
from myblog.models import UserInfo, BlogBody
from markdown import markdown
import urllib2
import StringIO, gzip
import xml.etree.ElementTree as Etree
import collections
import datetime
# 纪念
d1 = datetime.date(2012, 3, 5)
d2 = datetime.date.today()
dates = (d2 - d1).days


def index(request):  # 首页
    userinfo = UserInfo.objects.first()
    blog_body = BlogBody.objects.all().order_by('-blog_timestamp')[:6]
	# 热门文章
    hot_article = BlogBody.objects.all().order_by('-blog_clicknum')[:6]
    return render(request,
                  'home.html',
                  {'userinfo': userinfo, 'blog_body': blog_body, 'hot_article': hot_article, "dates": dates})


def is_alphabet(uchar):  # 判断unicode是否为英文
    if (uchar >= u'\u0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a'):
        return True
    else:
        return False


def weather(request):  # 查天气，空气质量
	# 热门文章
    hot_article = BlogBody.objects.all().order_by('-blog_clicknum')[:6]
    city = request.POST['city']
    if city.isspace():
        searchStatus = "error"
        return render(request, 'weather.html', {"searchStatus": searchStatus,
                                                'hot_article': hot_article, "dates": dates})
    elif city == "":
        searchStatus = "empty"
        return render(request, 'weather.html', {"searchStatus": searchStatus,
                                                'hot_article': hot_article, "dates": dates})
    elif is_alphabet(city):
        searchStatus = "pinyin"
        return render(request, 'weather.html', {"searchStatus": searchStatus,
                                                'hot_article': hot_article, "dates": dates})
    else:
        city = city.replace(" ", "")
        city = city.encode("utf-8")  # 接收表单提交的数据city是unicode类型，需要转化成str类型才行
        searchStatus = "success"
        url = "http://wthrcdn.etouch.cn/WeatherApi?city=" + city
        response = urllib2.urlopen(url)
        data = response.read()
        data = gzdecode(data)
        notify_data_tree = Etree.fromstring(data)
        weather = collections.OrderedDict()
        environment = collections.OrderedDict()
        try:
            weather['温度(单位℃)：'] = notify_data_tree.find("wendu").text
            weather['风力：'] = notify_data_tree.find("fengli").text
            weather['湿度：'] = notify_data_tree.find("shidu").text
            weather['数据更新时间：'] = notify_data_tree.find("updatetime").text
        except Exception:
            searchStatus = "noResult"
            return render(request,
                          'weather.html',
                          {'hot_article': hot_article,
                           "searchStatus": searchStatus, "dates": dates})
        try:
            environment['空气质量指数(AQI)：'] = notify_data_tree.find("environment/aqi").text
            environment['空气质量：'] = notify_data_tree.find("environment/quality").text
            environment['颗粒物(PM2.5)：'] = notify_data_tree.find("environment/pm25").text
            environment['颗粒物(PM10)：'] = notify_data_tree.find("environment/pm10").text
            environment['主要污染物：'] = notify_data_tree.find("environment/MajorPollutants").text
            environment['臭氧：'] = notify_data_tree.find("environment/o3").text
            environment['一氧化碳：'] = notify_data_tree.find("environment/co").text
            environment['二氧化氮：'] = notify_data_tree.find("environment/no2").text
            environment['二氧化硫：'] = notify_data_tree.find("environment/so2").text
            environment['室外活动建议：'] = notify_data_tree.find("environment/suggest").text
            environment['空气质量数据更新时间：'] = notify_data_tree.find("environment/time").text
        except Exception:
            searchStatus = "dijishi"
            return render(request,
                          'weather.html',
                          {'hot_article': hot_article,
                           "searchStatus": searchStatus,
                           "city": city,
                           "weather": weather, "dates": dates})
        return render(request,
                      'weather.html',
                      {'hot_article': hot_article,
                       "searchStatus": searchStatus,
                       "city": city,
                       "weather": weather,
                       "environment": environment, "dates": dates})


def gzdecode(data):  # gz解压缩
    compressedstream = StringIO.StringIO(data)
    gziper = gzip.GzipFile(fileobj=compressedstream)
    data2 = gziper.read()
    return data2


def article(request, blog_body_id=''):  # 全文展示
	# 热门文章
    hot_article = BlogBody.objects.all().order_by('-blog_clicknum')[:6]
    blog_content = BlogBody.objects.get(id=blog_body_id)
    num = blog_content.blog_clicknum
    num += 1
    blog_content.blog_clicknum = num
    blog_content.save()
    blog_content_body = markdown(blog_content.blog_body, ['codehilite'])
    return render(request, 'articleView.html', {'blog_content': blog_content, 'blog_content_body': blog_content_body, 'hot_article': hot_article, "dates": dates})


def about(request):  # 关于本站
	# 热门文章
    hot_article = BlogBody.objects.all().order_by('-blog_clicknum')[:6]
    return render(request, 'about.html')


def article_list(request, list_type, page):  # 分类页面
	# 热门文章
    hot_article = BlogBody.objects.all().order_by('-blog_clicknum')[:6]
    page = int(page)
    pre_page = page - 1
    next_page = page + 1
    pages = [x for x in range(1, get_pages(list_type) + 1)]
    end = pages[-1]
    content_list = BlogBody.objects.filter(blog_type=list_type).order_by('-blog_timestamp')[(page - 1) * 5: page * 5]
    if get_pages(list_type) > 1:
        return render(request, 'articleList.html',
                      {'content_list': content_list,
                       'list_type': list_type,
                       'pages': pages,
                       'end': end,
                       'page': page,
                       'pre_page': pre_page,
                       'next_page': next_page,
                       'errmsg': 'OK', 'hot_article': hot_article, "dates": dates}
                      )
    else:
        return render(request, 'articleList.html',
                      {'content_list': content_list,
                       'list_type': list_type,
                       'pages': pages,
                       'end': end,
                       'errmsg': 'faile', 'hot_article': hot_article, "dates": dates}
                      )


def get_pages(list_type):  # 计算总页数
    num = divmod(BlogBody.objects.filter(blog_type=list_type).count(), 5)
    if num[1] != 0:
        pages = num[0] + 1
    else:
        pages = num[0]
    return pages


def search_article(request):  # 搜索文章
	# 热门文章
    hot_article = BlogBody.objects.all().order_by('-blog_clicknum')[:6]
    keyword = request.POST['keyWord']
    if keyword.isspace():
        searchStatus = "error"
        return render(request, 'search.html', {"searchStatus": searchStatus,
                                               'hot_article': hot_article, "dates": dates})
    elif keyword == "":
        searchStatus = "empty"
        return render(request, 'search.html', {"searchStatus": searchStatus,
                                               'hot_article': hot_article, "dates": dates})
    else:
        keyword = keyword.replace(" ", "")
        keyword = keyword.lower()
        allArticle = BlogBody.objects.all()
        searchResult = []
        for x in allArticle:
            blog_title = x.blog_title.lower()
            blog_body = x.blog_body.lower()
            if keyword in blog_title:
                searchResult.append(x)
            elif keyword in blog_body:
                searchResult.append(x)
        searchStatus = "noResult" if len(searchResult) == 0 else "success"
        resultAmount = len(searchResult)
        return render(request, 'search.html', {"keyword": keyword,
                                               "searchResult": searchResult,
                                               "searchStatus": searchStatus,
                                               "resultAmount": resultAmount,
                                               'hot_article': hot_article, "dates": dates})


def search_by_tag(request, tag):  # 来自点击标签的搜索
	# 热门文章
    hot_article = BlogBody.objects.all().order_by('-blog_clicknum')[:6]
    keyword = tag.replace(" ", "")
    keyword = keyword.lower()
    allArticle = BlogBody.objects.all()
    searchResult = []
    for x in allArticle:
        blog_title = x.blog_title.lower()
        blog_body = x.blog_body.lower()
        if keyword in blog_title:
            searchResult.append(x)
        elif keyword in blog_body:
            searchResult.append(x)
    searchStatus = "noResult" if len(searchResult) == 0 else "success"
    resultAmount = len(searchResult)
    return render(request, 'search.html', {"keyword": keyword,
                                           "searchResult": searchResult,
                                           "searchStatus": searchStatus,
                                           "resultAmount": resultAmount,
                                           'hot_article': hot_article, "dates": dates})


def liuyan(request):  # 留言墙
	# 热门文章
    hot_article = BlogBody.objects.all().order_by('-blog_clicknum')[:6]
    return render(request, 'liuyan.html', {'hot_article': hot_article, "dates": dates})
