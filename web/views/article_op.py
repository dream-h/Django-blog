from django.shortcuts import render, redirect, HttpResponse
from django.db import transaction
from repository import models
from django.urls import reverse
from web.forms.article import ArticleForm
from web.auth import auth

import markdown
import json

from utils.xss import XSSFilter


@auth.check_login
def add_article(request, site):
    """
    添加文章
    :param request: 请求
    :param site: 博主
    :return:
    """
    # 从数据库中获取博客以及属于博客的分类，标签列表
    blog = models.Blog.objects.filter(site=site).select_related('user').first()
    #category_list = models.Category.objects.filter(blog=blog)
    #tag_list = models.Tag.objects.filter(blog=blog)
    if request.method == 'GET':
        article_form = ArticleForm(request=request)
        return render(
            request,
            'web_home/add_article.html',
            {
                'article_form': article_form,
                'blog': blog,
            }
        )
    else:
        #print(request.POST)
        article_form = ArticleForm(request=request, data=request.POST)
        if article_form.is_valid():
            # 获取验证后的数据
            article_post = article_form.cleaned_data
            #print(article_post)
            tags = article_post.pop('tags')
            #category_title = article_post.pop('category')
            article_body = article_post.pop('body')
            # 过滤掉白名单之外的标签
            #article_body = XSSFilter().process(article_body)
            #print(article_type_id)
            # 在文章表中添加文章记录
            article = models.Article.objects.create(blog=blog, **article_post)
            # 文章内容表与文章表是一对一的关系
            models.ArticleDetail.objects.create(
                content=article_body,
                article=article
            )
            tag_list = []
            for tag_id in tags:
                tag_id = int(tag_id)
                tag_list.append(models.Article2Tag(article=article, tag_id=tag_id))
            models.Article2Tag.objects.bulk_create(tag_list)
            return redirect('web:user_blog', site)

        else:
            print(article_form.errors)
            return render(
                request,
                'web_home/add_article.html',
                {
                    "article_form": article_form,
                    'blog': blog,
                }
            )


@auth.check_login
def edit_article(request, site, nid):
    """
    修改文章函数
    :param request:
    :param site:
    :param nid:
    :return:
    """
    blog = models.Blog.objects.get(site=site)
    if request.method == 'GET':
        article = models.Article.objects.get(nid=nid, blog=blog)
        if not article:
            return HttpResponse('没有这篇文章')
        tags = article.tags.values_list('nid')
        #print(tags)
        if tags:
            tags = list(zip(*tags))[0]
        init_article = {
                'title': article.title,
                'summary': article.summary,
                'body': article.articledetail.content,
                'article_type_id': article.article_type_id,
                'category_id': article.category_id,
                'tags': tags,
            }
        article_form = ArticleForm(request=request, data=init_article)
        return render(
                request,
                'web_home/edit_article.html',
                {
                    'article_form': article_form,
                    'nid': article.nid,
                    'blog': blog,
                 }
            )
    else:
        article_form = ArticleForm(request=request, data=request.POST)
        if article_form.is_valid():
            article_post = article_form.cleaned_data
            article = models.Article.objects.get(nid=nid, blog=blog)
            if not article:
                return HttpResponse('文章已经被删除')
            with transaction.atomic():
                body = article_post.pop('body')
                # 过滤掉白名单之外的标签
                #body = XSSFilter().process(body)
                tags = article_post.pop('tags')
                models.Article.objects.filter(nid=nid).update(**article_post)
                models.ArticleDetail.objects.filter(article=article).update(content=body)
                models.Article2Tag.objects.filter(article=article).delete()
                tag_list = []
                for tag_id in tags:
                    tag_id = int(tag_id)
                    tag_list.append(models.Article2Tag(article=article, tag_id=tag_id))
                print(tag_list)
                models.Article2Tag.objects.bulk_create(tag_list)
            return redirect('web_home:user_blog', site)
        else:
            return render(request, 'web_home/edit_article.html', {
                'article_form': article_form, 'nid': nid, 'blog': blog,
            })


@auth.check_login
def del_article(request, site, nid):
    """
    删除文章函数
    :param request:
    :param site:
    :param nid:
    :return:
    """
    blog = models.Blog.objects.get(site=site)
    article = models.Article.objects.get(nid=nid, blog=blog)
    print(article)
    detail = models.ArticleDetail.objects.filter(article=article).delete()
    print(detail)
    models.Article2Tag.objects.filter(article=article).delete()
    article.delete()
    return redirect('web_home:user_blog', site)


@auth.check_login
def article_detail(request, site, nid):
    """
    文章详情显示
    :param request:
    :return:
    """
    # 从数据库中获取博客以及属于博客的分类，标签列表
    blog = models.Blog.objects.filter(site=site).select_related('user').first()
    category_list = models.Category.objects.filter(blog=blog)
    tag_list = models.Tag.objects.filter(blog=blog)

    article = models.Article.objects.filter(nid=nid, blog=blog).select_related('category', 'articledetail').first()
    comment_list = models.Comment.objects.filter(article=article).select_related('reply')


    article_body = article.articledetail.content
    print(article_body)
    # 用Markdown语法渲染成HTML样式
    article_body = markdown.markdown(article_body,
        extensions=[
            # 包含 缩写、表格等常用扩展
            'markdown.extensions.extra',
            # 语法高亮扩展
            'markdown.extensions.codehilite',
        ]
    )
    print(article_body)


    return render(
        request,
        'web_home/article_detail.html',
        {
            'category_list': category_list,
            'tag_list': tag_list,
            'blog': blog,
            'article': article,
            'article_body': article_body,
            'comment_list': comment_list,
            'site': site,
        }
    )