from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponse
from django.utils.safestring import mark_safe
from django.views.decorators.cache import cache_page
from .util import visit, visit_type, paging, PAGE_SIZE
# Create your views here.


# @cache_page(60 * 15)
def home(request):
    articles = Article.objects.filter(classification__name="blog").order_by("-date")
    return render(request, "home.html", {"articles": articles})


@cache_page(60)
def show(request):

    # 按id获取文章
    if request.GET.get('pk', -1) != -1:
        pk = request.GET.get('pk')
        art = Article.objects.get(id=pk)
        art.volume += 1
        art.save()
        art.html_content = mark_safe(art.html_content)
        visit(visit_type["ARTICLE"], request, "访问了id为"+pk+"的文章")
        return render(request, "show.html", {"article": art})

    return HttpResponse("搞不懂你的请求")


def search(request):
    # 关键字搜索
    if request.GET.get('q', -1) != -1:
        q = request.GET.get('q')
        articles = Article.objects.filter(Q(content__icontains=q) |
                                          Q(title__icontains=q) |
                                          Q(description__icontains=q)).order_by("-date")
        visit(visit_type["ARTICLE"], request, "搜索了" + q)
        # 分页
        page_count = round(articles.count() / PAGE_SIZE)
        page_num = request.GET.get('page_num')
        articles = paging(articles, page_num)
        return render(request, "showlist.html", {"articles": articles, "page_count": list(range(page_count)),
                                                 "cur_page": page_num})
    return HttpResponse("搞不懂你的请求")


# note, blog, rss, link
def note(request):
    classification = "note"
    articles = Article.objects.filter(classification__name=classification).order_by("-date")
    # 如果只有一篇文章，则显示文章
    if len(articles) == 1:
        article = articles[0]
        article.volume += 1
        article.save()
        article.html_content = mark_safe(article.html_content)
        visit(visit_type["OTHERS"], request, "访问了" + article.title)
        return render(request, "show.html", {"article": article})
    visit(visit_type["OTHERS"], request, "访问了" + classification + "文章列表")
    # 分页
    page_count = round(articles.count()/PAGE_SIZE)
    page_num = request.GET.get('page_num', 1)
    articles = paging(articles, page_num)
    return render(request, "showlist.html", {"articles": articles, "page_count": list(range(page_count)),
                                             "cur_page": int(page_num), "class": classification})


def blog(request):
    classification = "blog"
    articles = Article.objects.filter(classification__name=classification).order_by("-date")
    # 如果只有一篇文章，则显示文章
    if len(articles) == 1:
        article = articles[0]
        article.html_content = mark_safe(article.html_content)
        visit(visit_type["OTHERS"], request, "访问了" + article.title)
        return render(request, "show.html", {"article": article})
    visit(visit_type["OTHERS"], request, "访问了" + classification + "文章列表")
    # 分页
    page_count = round(articles.count() / PAGE_SIZE)
    page_num = request.GET.get('page_num')
    articles = paging(articles, page_num)
    return render(request, "showlist.html", {"articles": articles, "page_count": list(range(page_count)),
                                             "cur_page": page_num, "class": classification})


def link(request):
    classification = "link"
    articles = Article.objects.filter(classification__name=classification).order_by("-date")
    # 如果只有一篇文章，则显示文章
    if len(articles) == 1:
        article = articles[0]
        article.volume += 1
        article.save()
        article.html_content = mark_safe(article.html_content)
        visit(visit_type["OTHERS"], request, "访问了" + article.title)
        return render(request, "show.html", {"article": article})
    visit(visit_type["OTHERS"], request, "访问了" + classification + "文章列表")
    # 分页
    page_count = round(articles.count() / PAGE_SIZE)
    page_num = request.GET.get('page_num')
    articles = paging(articles, page_num)
    return render(request, "showlist.html", {"articles": articles, "page_count": list(range(page_count)),
                                             "cur_page": page_num, "class": classification})


def tag(request):
    # 按标签获取
    if request.GET.get('tag', -1) != -1:
        tag = request.GET.get('tag')
        articles = Article.objects.filter(tags__name=tag).order_by("-date")
        visit(visit_type["OTHERS"], request, "访问了" + tag + "文章列表")
        # 分页
        page_count = articles.count() // PAGE_SIZE + 1
        page_num = request.GET.get('page_num')
        articles = paging(articles, page_num)
        return render(request, "showlist.html", {"articles": articles, "page_count": list(range(page_count)),
                                                 "cur_page": page_num})
    return HttpResponse("搞不懂你的请求")


def about(request):
    classification = "about"
    articles = Article.objects.filter(classification__name=classification).order_by("-date")
    # 如果只有一篇文章，则显示文章
    if len(articles) == 1:
        article = articles[0]
        article.volume += 1
        article.save()
        article.html_content = mark_safe(article.html_content)
        visit(visit_type["OTHERS"], request, "访问了" + article.title)
        return render(request, "show.html", {"article": article})
    visit(visit_type["OTHERS"], request, "访问了" + classification + "文章列表")
    # 分页
    page_count = round(articles.count() / PAGE_SIZE)
    page_num = request.GET.get('page_num')
    articles = paging(articles, page_num)
    return render(request, "showlist.html", {"articles": articles, "page_count": list(range(page_count)),
                                             "cur_page": page_num, "class": classification})


from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Article


class BlogFeed(Feed):
    title = "丁丁哈哈的博客"
    link = "/show/"
    description = "一只垃圾的網站."

    def description(self, obj):
        return self.description

    def items(self):
        return Article.objects.all().order_by("-date")

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return self.link + "?pk=" + str(item.id)

    def item_updateddate(self, item):
        import datetime
        date = [int(i) for i in str(item.date).split(" ")[0].split("-")]
        return datetime.datetime(date[0], date[1], date[2])
