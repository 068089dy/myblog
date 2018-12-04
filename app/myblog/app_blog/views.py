from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponse
from django.utils.safestring import mark_safe
from django.views.decorators.cache import cache_page
from .CommonViews import PageListView
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


class Search(PageListView):

    def victim(self):
        self.root_router = "search"
        self.classification = "search"
        self.articles = None
        self.cur_page = self.data.GET.get('page_num', 1)
        if self.data.GET.get('q', -1) == -1:
            return -1
        q = self.data.GET.get('q', -1)
        # self.articles = Article.objects.filter(tags__name=tag).order_by("-date")
        self.articles = Article.objects.filter(Q(content__icontains=q) |
                                          Q(title__icontains=q) |
                                          Q(description__icontains=q)).order_by("-date")


class Note(PageListView):

    def victim(self):
        self.root_router = "note"
        self.classification = "note"
        self.articles = None
        self.cur_page = self.data.GET.get('page_num', 1)
        self.articles = Article.objects.filter(classification__name=self.classification).order_by("-date")


class Blog(PageListView):

    def victim(self):
        self.root_router = "blog"
        self.classification = "blog"
        self.articles = None
        self.cur_page = self.data.GET.get('page_num', 1)
        self.articles = Article.objects.filter(classification__name=self.classification).order_by("-date")


class Link(PageListView):

    def victim(self):
        self.root_router = "link"
        self.classification = "link"
        self.articles = None
        self.cur_page = self.data.GET.get('page_num', 1)
        self.articles = Article.objects.filter(classification__name=self.classification).order_by("-date")


class Tag(PageListView):

    def victim(self):
        self.root_router = "tag"
        self.classification = "tag"
        self.articles = None
        self.cur_page = self.data.GET.get('page_num', 1)
        if self.data.GET.get('tag', -1) == -1:
            return None
        tag = self.data.GET.get('tag', -1)
        self.articles = Article.objects.filter(tags__name=tag).order_by("-date")


class About(PageListView):

    def victim(self):
        self.root_router = "about"
        self.classification = "about"
        self.articles = None
        self.cur_page = self.data.GET.get('page_num', 1)
        self.articles = Article.objects.filter(classification__name=self.classification).order_by("-date")


from django.contrib.syndication.views import Feed
from .models import Article


class BlogFeed(Feed):
    title = "丁丁哈哈的博客"
    link = "/show/"
    description = "一只垃圾的網站."

    def description(self, obj):
        return self.description

    def items(self):
        return Article.objects.filter(classification__name="blog").order_by("-date")

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
