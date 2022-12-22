from django.shortcuts import render,get_object_or_404, redirect
from .models import Blog,Comment
from .forms import CommentForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect




def all_blogs(request):
    blogs = Blog.objects.order_by('-id')
    blog_count = Blog.objects.count
    return render(request,'Blog/all_blog.html',{'blogs':blogs,'blog_count':blog_count})


def detail(request,blog_id):
    
    posts = get_object_or_404(Blog, pk= blog_id)
    blog_desc = Blog.objects.all()
    comments = posts.comments.filter(active=True).order_by('-created')[:30]
    comment_form =CommentForm()
    return render(request,'Blog/viewblog.html',{'posts':posts,'comments':comments,
                'comment_form':comment_form,'blog_desc':blog_desc})
       



def post_comment(request,blog_id):
    posts= get_object_or_404(Blog,pk=blog_id)
    #comments = posts.comments.filter(active=True)
    if request.method=='POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment=comment_form.save(commit=False)
            new_comment.post= posts
            new_comment.save()
        return HttpResponseRedirect('view')    
        #return redirect('detail')
    else:
        comment_form= CommentForm()
        return render(request,'Blog/viewblog.html',{'comment_form':comment_form})