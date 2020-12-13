from django.shortcuts import render, get_object_or_404
from .models import Blog, BlogType


def blog_list(request):
    context = {}
    context['blogs'] = Blog.objects.all()
    context['blog_count'] = Blog.objects.all().count()
    return render(request,'blog/blog_list.html',context)

def blog_detail(request, blog_pk):
    context = {}
    context['blog'] = get_object_or_404(Blog, id=blog_pk)
    return render(request, 'blog/blog_detail.html', context)

def blogs_with_type(request, blog_type_pk):
    context = {}
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    context['blogs'] = Blog.objects.filter(blog_type=blog_type)
    context['blog_type'] = blog_type
    return render(request, 'blog/blogs_with_type.html', context)

""" def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('user_name')
        pwd = request.POST.get('pwd')
        rem_name = request.POST.get('rem_name')

        user = authenticate(username=username, password=pwd)
        if user:
            login(request, user)
            response = redirect(reverse('goods:index'))
            if rem_name == 'on':
                response.set_cookie('uname', username)

            return response
        else:
            return render(request, 'user/login.html', {'errmsg': '用户名或者密码有误'})
    else:
        username = request.COOKIES.get('uname', '')
        return render(request, 'user/login.html', {'username': username})
 """