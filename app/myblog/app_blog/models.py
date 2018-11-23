from django.db import models
import django.utils.timezone as timezone

# Create your models here.
from mdeditor.fields import MDTextField


class Article(models.Model):
    # 是否显示
    display = models.BooleanField(default=True)
    # 标题
    title = models.CharField(max_length=100)
    # 描述
    description = models.CharField(max_length=200)
    # 分类
    classification = models.ForeignKey("Classification", null=True, on_delete=models.SET_NULL, related_name="classification")
    # 标签
    tags = models.ManyToManyField("Tag", related_name='tags')
    # 日期
    date = models.DateTimeField(default=timezone.now)
    # 内容
    content = MDTextField()
    # html内容
    html_content = models.TextField(blank=True, null=True)
    # 阅读量
    volume = models.IntegerField(default=0)

    # def save(self, *args, **kwargs):
    #     self.html_content = self.content
    #     super(Articles, self).save(*args, **kwargs)
    class Meta:
        db_table = 'blog_article'

    def __str__(self):
        return self.title


class Comment(models.Model):
    # models.CASCADE是级联删除
    article = models.ForeignKey("Article", on_delete=models.CASCADE)
    # 如果null为True，django会用null来存储空值
    # blank和null一样，只不过blank只与验证相关，而null是与数据库相关的，如果blank=False，则后台表单必填
    father = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(auto_now=True)
    username = models.CharField(max_length=50)
    email = models.EmailField(blank=False)
    content = models.TextField(blank=False)
    device = models.TextField(blank=False)

    class Meta:
        db_table = 'blog_comment'

    def __str__(self):
        return self.content


class Visitor(models.Model):

    # class Meta:
    #     abstract = True
    #
    # @classmethod
    # def setDb_table(cls, tableName):
    #     class Meta:
    #         # db_table指定在数据库中，当前模型生成的数据表的表名。
    #         db_table = tableName
    #
    #     attrs = {
    #         '__module__': cls.__module__,
    #         'Meta': Meta
    #     }
    #     return type(tableName, (cls,), attrs)

    # 访问者ip
    ip_address = models.GenericIPAddressField()
    # 访问日期
    date = models.DateTimeField(default=timezone.now)
    # 访问类别，文章或评论
    type = models.CharField(max_length=50)
    # 备注
    remark = models.CharField(max_length=100)

    class Meta:
        db_table = 'blog_visitor'

    def __str__(self):
        return self.ip_address


class Classification(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, blank=True, null=True)
    # 日期
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "blog_classification"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, blank=True, null=True)
    # 日期
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "blog_tag"

    def __str__(self):
        return self.name



