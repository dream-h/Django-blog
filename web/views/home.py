#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.shortcuts import render, redirect
from repository import models
from django.urls import reverse
from utils.pagination import Pagination


def index(request, *args, **kwargs):
    """
    博客首页：展现全部博文
    :param request:
    :return:
    """
    """
    type_choice = [
        (1, 'Python'),
        (2, 'Django'),
        (3, 'book'),
        (4, '区块链'),
        (5, '人工智能'),
    ]
    """
    print(kwargs)
    article_type_list = models.Article.type_choice
    if kwargs:
        article_type_id = int(kwargs['article_type_id'])
        base_url = reverse('web_home:index', kwargs=kwargs)
        print(article_type_id)
        data_count = models.Article.objects.filter(article_type_id=article_type_id).count()
        print(data_count)
        page_obj = Pagination(request.GET.get('p'), data_count)
        # 每页文章列表
        article_list = models.Article.objects.filter(article_type_id=article_type_id).order_by('-nid')[page_obj.start:page_obj.end]
        page_str = page_obj.page_str(base_url)
    else:
        article_type_id = None
        base_url = '/'
        data_count = models.Article.objects.all().count()

        page_obj = Pagination(request.GET.get('p'), data_count)
        # 每页文章列表
        article_list = models.Article.objects.all().order_by('-nid')[page_obj.start:page_obj.end]
        page_str = page_obj.page_str(base_url)

    return render(
        request,
        'web_home/index.html',
        {
            'article_type_id': article_type_id,
            'article_type_list': article_type_list,
            'article_list': article_list,
            'page_str': page_str,
        }
    )


def get_date_time():
    """
    从数据库中取出以%Y-%m的时间格式筛选的date_list
    :return:
    """
    import sqlite3
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("""select nid, count(nid) as nm, strftime("%Y-%m",created_time) as crtime from repository_article group by crtime""")
    date_list = cursor.fetchall()
    conn.close()
    #print(date_list)
    return date_list


def user_blog(request, site):
    """
    用户博客个人主页
    :param request:
    :param site: 博主前缀
    :return:
    """
    blog = models.Blog.objects.filter(site=site).select_related('user').first()
    if not blog:
        return redirect('/')

    # 获取博客主页的标签，分类
    tag_list = models.Tag.objects.filter(blog=blog)
    category_list = models.Category.objects.filter(blog=blog)
    date_list = get_date_time()
    '''
    date_list = models.Article.objects.raw(
        'select nid, count(nid) as nm,\
        strftime("%Y-%m",created_time) as ctime\
        from repository_article group by ctime'
    )
    '''
    article_list = models.Article.objects.filter(blog=blog).all()

    return render(
        request,
        'web_home/user_blog_home.html',
        {
            'blog': blog,
            'tag_list': tag_list,
            'category_list': category_list,
            'date_list': date_list,
            'article_list': article_list,
        }
    )


def article_filter(request, site, condition, nid):
    """
    个人博客主页筛选
    :param request: 请求
    :param site: 个人博客前缀
    :param condition: 筛选方式
    :param nid: 筛选方式中的id
    :return:
    """
    blog = models.Blog.objects.filter(site=site).select_related('user').first()
    if not blog:
        redirect('/')
    category_list = models.Category.objects.filter(blog=blog)
    tag_list = models.Tag.objects.filter(blog=blog)
    date_list = get_date_time()

    if condition == 'category':
        article_list = models.Article.objects.filter(category_id=nid, blog=blog).all()
    elif condition == 'tag':
        article_list = models.Article.objects.filter(tags=nid, blog=blog).all()
    else:
        #val = str(nid)
        #print(val)
        article_list = models.Article.objects.filter(blog=blog).extra(
            where=['strftime("%%Y-%%m",created_time)=%s'], params=[nid, ]).all()
    return render(
        request,
        'web_home/user_blog_home.html',
        {
            'blog': blog,
            'category_list': category_list,
            'tag_list': tag_list,
            'date_list': date_list,
            'article_list': article_list,
        }
    )


def user_article_list(request, *args, **kwargs):
    """
        博主个人文章管理
        :param request:
        :return:
        """
    blog_id = request.session['user_info']['blog__nid']
    blog = models.Blog.objects.get(nid=blog_id)
    condition = {}
    for k, v in kwargs.items():
        if v == '0':
            pass
        else:
            condition[k] = v
    condition['blog_id'] = blog_id
    data_count = models.Article.objects.filter(**condition).count()
    page = Pagination(request.GET.get('p', 1), data_count)
    result = models.Article.objects.filter(**condition).order_by('-nid').only('nid', 'title', 'blog').select_related(
        'blog')[page.start:page.end]
    page_str = page.page_str(reverse('web_home:article', kwargs=kwargs))
    category_list = models.Category.objects.filter(blog_id=blog_id).values('nid', 'title')
    type_list = map(lambda item: {'nid': item[0], 'title': item[1]}, models.Article.type_choice)
    kwargs['p'] = page.current_page
    return render(request,
                  'web_home/user_article_list.html',
                  {'result': result,
                   'page_str': page_str,
                   'category_list': category_list,
                   'type_list': type_list,
                   'arg_dict': kwargs,
                   'data_count': data_count,
                   'blog': blog,
                   }
                  )








