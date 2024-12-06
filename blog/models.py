from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
import markdown
from django.utils.html import strip_tags


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
    


    


# Create your models here.
