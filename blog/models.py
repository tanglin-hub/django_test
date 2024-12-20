from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
import markdown
from django.utils.html import strip_tags
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
import re
from django.utils.functional import cached_property

class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class Tag(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField('标题', max_length=70)  # 标题字段
    body = models.TextField('正文')              # 内容字段
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    modified_time = models.DateTimeField('修改时间')     # 更新时间
    excerpt = models.CharField('摘要', max_length=200, blank=True)
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    views=models.PositiveIntegerField(default=0, editable=False)
    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering=['-created_time']
    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()
        md=markdown.Markdown(extension=[
            'markdown.extensions.extra'
            'markdown.extensions.codehilite'
        ])
        self.excerpt=strip_tags(md.convert(self.body))[:54]
        super().save(*args, **kwargs)
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={"pk": self.pk})
    def increase_views(self):
        self.views +=1
        self.save(update_fields=['views'])
    def generate_rich_content(value):
        md=markdown.Markdown(extensions=[
            'markdown.extensions.toc',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ])
        content=md.convert(value)
        m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
        toc=m.group(1) if m is not None else ''
        return{"content":content, "toc":toc}
    
    @property
    def toc(self):
        return self.rich_content.get("TOC", "")
    
    @property
    def body_html(self):
        return self.rich_content.get("content", "")
    
    @cached_property
    def rich_content(self):
        return generate_rich_content(self.body)
    


    


# Create your models here.
