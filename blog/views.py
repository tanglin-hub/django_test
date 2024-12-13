from django.shortcuts import render,get_object_or_404
from .models import Post,Category,Tag
import markdown
import re
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.views.generic import ListView, DetailView
from pure_pagination.mixins import PaginationMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Q

# Create your views here.
class IndexView(PaginationMixin, ListView):
    model=Post
    template_name='blog/index.html'
    context_object_name='post_list'
    paginate_by=5

class CategoryView(ListView):
#    model=Post
#    template_name='blog/index.html'
#    context_object_name='post_list'
    def get_queryset(self):
        cate=get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)
    
class ArchiveView(ListView):
    model=Post
    template_name='blog/index.html'
    context_object_name='post_list'
    def get_queryset(self):
        year=self.kwargs('year')
        month=self.kwargs('month')
        return super(ArchiveView, self).get_queryset().filter(created_time__year=year, created_time__month=month)

class TagView(ListView):
    model=Post
    template_name='blog/index.html'
    context_object_name='post_list'
    def get_queryset(self):
        t=get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=t)
    
class PostDetailView(DetailView):
    model=Post
    template_name='blog/detail.html'
    context_object_name='post'
    def get_object(self, queryset=None):
        post=super().get_object(queryset=None)
        md=markdown.Markdown(extensions=[ 
            'markdown.extensions.toc',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
            ])
        post.body=md.convert(post.body)
        m=re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
        post.toc=m.group(1) if m is not None else ''
        print(post)
        return post
    
    def get(self, request, *args, **kwargs):
        response=super(PostDetailView, self).get(request, *args, **kwargs)
        
        return response

def search(request):
    q=search.GET.get('q')
    if not q:
        error_msg="请输入关键词"
        messages.add_message(request, messages.ERROR, error_msg, extra_tags='danger')
        return redirect('blog:index')
    post_list=Post.objects.filter(Q(title__icontains=q | Q(body__icontains=q)))
    return render(request, 'blog/index.html',  {'post_list':post_list})