from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.utils.safestring import mark_safe
from .util import visit, paging, PAGE_SIZE


class PageListView(View):

    def __init__(self):
        self.classification = ""    #当前分类
        self.root_router = ""       #根路由
        self.page_size = PAGE_SIZE  #分页大小
        self.articles = None        #文章querysets
        self.cur_page = 1           #当前页
        self.data = None            #请求数据
        self.result = {
            # "articles": self.articles,
            # "page_count": list(range(self.page_count)),
            # "cur_page": self.cur_page,
            # "root_router": self.root_router,
            # "class": self.classification,
        }

    def victim(self):
        pass
        '''
        Eg:
        
        '''
        # self.data.get['pk']
        # self.root_router = ""
        # self.classification = ""
        # self.articles = None
        # if self.data.GET.get('page_num', -1) == -1:
        #     return None
        # self.cur_page = self.data.GET.get('pk', -1)
        # if self.data.GET.get('tag', -1) == -1:
        #     return None
        # tag = self.self.data.GET.get('tag', -1)
        # self.articles = Article.objects.filter(tags__name=tag).order_by("-date")

    def get(self, request):
        self.data = request
        if self.victim() == -1:
            return HttpResponse("搞不懂你的请求！")

        # 如果只有一篇文章，则显示文章
        # if len(self.articles) == 1:
        #     article = self.articles[0]
        #     article.volume += 1
        #     article.save()
        #     article.html_content = mark_safe(article.html_content)
        #     visit(self.classification, request, "访问了" + article.title)
        #     return render(request, "show.html", {"article": article})
        visit(self.classification, request, "访问了" + self.classification + "文章列表")
        # 分页
        page_count = round(self.articles.count() / self.page_size)
        page_num = request.GET.get('page_num', 1)
        articles = paging(self.articles, page_num)

        self.result = {
            "articles": articles,
            "page_count": list(range(page_count)),
            "cur_page": self.cur_page,
            "root_router": self.root_router,
            "class": self.classification,
        }
        return render(request, "showlist.html", self.result)
