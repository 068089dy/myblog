from django.contrib import admin
from .models import Article, Comment, Tag, Classification, Visitor
import requests
import json
from .forms import ArticleForm
# Register your models here.


class VisitorAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'date', 'remark')


@admin.register(Classification)
class ClassificationAdmin(admin.ModelAdmin):
    list_display = ("name", "date", "description")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "date", "description")


admin.site.register(Visitor, VisitorAdmin)


# 注册数据表Articles
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):


    list_display = ('date', 'title', 'volume')
    # fields = ['title', 'description', 'tags', 'content']
    form = ArticleForm
    fieldsets = (
        (u'基本信息', {
            'fields': (
                ('title', 'description', 'classification', ),  # 一行
                ('tags', 'date'),  # 另一行
                # 新一行
            ),
            'classes': ('person',),  # html 标签的 class 属性
        }),
        (u'内容', {  # 另一个 fieldset
            'fields': (
                ('content',),
            ),
        }),
    )
    '''
    重写model保存方法
    @param
    @request：请求实例
    @obj:Articles model实例
    @form：提交表单
    @change：改变
    '''
    def save_model(self, request, obj, form, change):
        # 获取Article的html_content字段
        obj.html_content = self.md2html(obj.content)
        super().save_model(request, obj, form, change)

    '''
    通过github api将markdown转化为html
    '''

    def md2html(self, md: str):
        return requests.post("https://api.github.com/markdown",
                             data=json.dumps({"text": md, "mode": "markdown"}),
                             headers={'Content-Type': 'application/json'}).text
