from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponse
from django.utils.safestring import mark_safe
from django.views.decorators.cache import cache_page
from .util import visit, visit_type
# Create your views here.

from django.core import serializers
from .models import Article


# @cache_page(60 * 15)
def home(request):
    articles = Article.objects.filter(classification__name="blog").order_by("-date")
    return render(request, "home.html", {"articles": articles})


@cache_page(60)
def show(request):
    # 关键字搜索
    if request.GET.get('q', -1) != -1:
        q = request.GET.get('q')
        articles = Article.objects.filter(Q(content__icontains=q) |
            Q(title__icontains=q) |
            Q(description__icontains=q)).order_by("-date")
        visit(visit_type["ARTICLE"], request, "搜索了"+q)
        return render(request, "showlist.html", {"articles": articles})
    # 按id获取文章
    if request.GET.get('pk', -1) != -1:
        pk = request.GET.get('pk')
        art = Article.objects.get(id=pk)
        art.volume += 1
        art.save()
        art.html_content = mark_safe(art.html_content)
        visit(visit_type["ARTICLE"], request, "访问了id为"+pk+"的文章")
        return render(request, "show.html", {"article": art})
    # 获取文章分类列表，如果只有一篇文章，则显示文章
    if request.GET.get('class', -1) != -1:
        classification = request.GET.get('class')
        articles = Article.objects.filter(classification__name=classification).order_by("-date")
        # 如果只有一篇文章，则显示文章
        if len(articles) == 1:
            article = articles[0]
            article.html_content = mark_safe(article.html_content)
            visit(visit_type["OTHERS"], request, "访问了"+article.title)
            return render(request, "show.html", {"article": article})
        visit(visit_type["OTHERS"], request, "访问了"+classification+"文章列表")
        return render(request, "showlist.html", {"articles": articles})
    return HttpResponse("搞不懂你的请求")





