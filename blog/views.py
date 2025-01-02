import json
from .filters import PostFilter, BlogFilter
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import *
from .forms import *
# Create your views here.


def blogs(request):
    blogs = Blog.objects.filter(public=True, published=True)
    filter = BlogFilter(request.GET, queryset = blogs)
    blogs = filter.qs

    context = {
        "blogs" : blogs,
        "filter": filter
    }
    return render(request, "blogs.html", context)

def posts(request):
    posts = Post.objects.filter(blog__public = True, published=True)
    filter = PostFilter(request.GET, queryset = posts)
    posts = filter.qs

    context = {
        "posts" : posts,
        "filter": filter
    }
    return render(request, "posts.html", context)


def blog(request, slug):
    blog = Blog.objects.get(name=slug)
    posts = Post.objects.filter(blog=blog)
    topics = Topic.objects.filter(blog=blog)
    filter = PostFilter(request.GET, queryset=posts)
    posts = filter.qs
    context = {
        "blog": blog,
        "topics": topics,
        "posts": posts,
        "filter": filter
    }
    return render(request, "blog.html", context)


def post(request,slug, id):
    post = Post.objects.get(id=id)
    elements = Element.objects.filter(post=post)
    context = {
        "post": post,
        "elements": elements
    }
    return render(request, "post.html", context)


def publish_post(request, slug, id):
    post = Post.objects.get(id=id)
    if post.blog.user == request.user.profile and not post.published:
        post.published = True
        post.save()
        return redirect(f"/blogs/{post.blog.name}")
    else:
        return redirect("/Error")


@login_required
def create_blog(request):
    if request.method == "POST":
        form = CreateBlog(request.POST, request.FILES)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.user = request.user.profile
            myform.save()
            return redirect(f"/blogs/{myform.name}")
    else:
        form = CreateBlog()

    context = {
        "form": form
    }
    return render(request, "create_blog.html", context)


@login_required
def delete_blog(request, slug):
    user = request.user.profile
    blog = Blog.objects.get(name=slug)
    if blog.user == user:
        blog.delete()
        return redirect("/")
    else:
        return redirect("/Error")


@login_required
def add_post(request, slug):
    blog = Blog.objects.get(name=slug)
    if request.user.profile == blog.user:
        if request.method == "POST":
            form = AddPost(request.POST, request.FILES, blog=blog)
            if form.is_valid():
                myform = form.save(commit=False)
                myform.blog = blog
                myform.save()
                return redirect(f'/blogs/{blog.name}')
        else:
            form = AddPost(blog=blog)

        context = {
            "blog": blog,
            "form": form
        }
        return render(request, "add_post.html", context)
    else:
        return redirect("/Error")


@login_required
def delete_post(request, slug, id):
    user = request.user.profile
    post = Post.objects.get(id=id)
    name = post.blog.name
    if post.blog.user == user:
        post.delete()
        return redirect(f"/blogs/{name}")
    else:
        return redirect("/Error")


@login_required
def add_heading(request, slug, id):
    post = Post.objects.get(id=id)
    if request.user.profile == post.blog.user:
        if request.method == "POST":
            form = AddHeading(request.POST)
            if form.is_valid():
                myform = form.save()
                heading = Heading.objects.get(id=myform.id)
                Element.objects.create(type="heading", post=post, heading=heading)
                return redirect(f"/blogs/{post.blog.name}/posts/{post.id}")
        else:
            form = AddHeading()

        context = {
            "form": form
        }
        return render(request, "add_heading.html", context)
    else:
        return redirect("/Error")


@login_required
def add_link(request, slug, id):
    post = Post.objects.get(id=id)
    if request.user.profile == post.blog.user:
        if request.method == "POST":
            form = AddLink(request.POST, request.FILES)
            if form.is_valid():
                myform = form.save()
                link = Link.objects.get(id=myform.id)
                Element.objects.create(type="link", post=post, link=link)
                return redirect(f"/blogs/{post.blog.name}/posts/{post.id}")
        else:
            form = AddLink()

        context = {
            "form": form
        }
        return render(request, "add_link.html", context)
    else:
        return redirect("/Error")

@login_required
def add_topic(request, slug):
    blog = Blog.objects.get(name=slug)
    if request.user.profile == blog.user:
        if request.method == "POST":
            form = AddClass(request.POST, request.FILES)
            if form.is_valid():
                myform = form.save(commit=False)
                myform.blog = blog
                myform.save()
                return redirect(f"/blogs/{blog.name}/posts/create")
        else:
            form = AddClass()

        context = {
            "form": form
        }
        return render(request, "add_topic.html", context)
    else:
        return redirect("/Error")
    
@login_required
def add_frame(request, slug, id):
    post = Post.objects.get(id=id)
    if request.user.profile == post.blog.user:
        if request.method == "POST":
            form = AddFrame(request.POST, request.FILES)
            if form.is_valid():
                myform = form.save()
                source = Iframe.objects.get(id=myform.id)
                Element.objects.create(type="frame", post=post, frame=source)
                return redirect(f"/blogs/{post.blog.name}/posts/{post.id}")
        else:
            form = AddFrame()

        context = {
            "form": form
        }
        return render(request, "add_frame.html", context)
    else:
        return redirect("/Error")


@login_required
def add_image(request, slug, id):
    post = Post.objects.get(id=id)
    if request.user.profile == post.blog.user:
        if request.method == "POST":
            try: 
                file = request.FILES["file"]
            except:
                file = None
            url = request.POST["src"] if request.POST["src"] else None
            if bool(file) != bool(url):
                myform = Image.objects.create(file=file, src=url)
                img = Image.objects.get(id=myform.id)
                Element.objects.create(type="image", post=post, image=img)
                return redirect(f"/blogs/{post.blog.name}/posts/{post.id}")
            else:
                return redirect(f"/blogs/{post.blog.name}/posts/{post.id}/addImage")

        return render(request, "add_image.html")
    else:
        return redirect("/Error")


@login_required
def add_list(request, slug, id):
    post = Post.objects.get(id=id)
    if request.user.profile == post.blog.user:
        if request.method == "POST":
            form = AddList(request.POST, request.FILES)
            if form.is_valid():
                myform = form.save()
                lst = List.objects.get(id=myform.id)
                Element.objects.create(type="list", post=post, list=lst)
                return redirect(f"/blogs/{post.blog.name}/posts/{post.id}")
        else:
            form = AddList()

        context = {
            "form": form
        }
        return render(request, "add_list.html", context)
    else:
        return redirect("/Error")


@login_required
def add_paragraph(request, slug, id):
    post = Post.objects.get(id=id)
    if request.user.profile == post.blog.user:
        if request.method == "POST":
            form = AddParagraph(request.POST, request.FILES)
            if form.is_valid():
                myform = form.save()
                p = Paragraph.objects.get(id=myform.id)
                Element.objects.create(type="paragraph", post=post, p=p)
                return redirect(f"/blogs/{post.blog.name}/posts/{post.id}")
        else:
            form = AddParagraph()

        context = {
            "form": form
        }
        return render(request, "add_paragraph.html", context)
    else:
        return redirect("/Error")


@login_required
def add_line(request, slug, id):
    post = Post.objects.get(id=id)
    if request.user.profile == post.blog.user:
        Element.objects.create(type="line", post=post)
        return redirect(f"/blogs/{post.blog.name}/posts/{post.id}")
    else:
        return redirect("/Error")


@login_required
def add_item(request, slug, id, lid):
    post = Post.objects.get(id=id)
    lst = List.objects.get(id=lid)
    element = Element.objects.get(list=lst)
    if request.user.profile == element.post.blog.user:
        if request.method == "POST":
            form = AddItem(request.POST, request.FILES)
            if form.is_valid():
                myform = form.save(commit=False)
                myform.list = lst
                myform.save()
                return redirect(f"/blogs/{post.blog.name}/posts/{post.id}")
            else:
                print(form.errors)
        else:
            form = AddItem()

        context = {
            "form": form,
        }

        return render(request, "add_item.html", context)

    else:
        return redirect("/Error")


@login_required
def publish(request, slug):
    # blog = Blog.objects.get(name=slug)
    # if blog.user != request.user.profile:
    #     print("you don't own this blog")
    #     return redirect("/Error")
    # context = {
    #     "website": blog
    # }
    # return render(request, "publish_blog.html", context)

    return redirect("/Error")

@login_required
def paymentComplete(request):
    # #print('REQUEST BODY:', request.body)
    # body = json.loads(request.body)
    # #print('BODY:', body)
    # website_unique_name = body['site_name']
    # #print(website_unique_name)
    # website = Blog.objects.get(name=website_unique_name)
    # #print(website.type)
    # website.published = True
    # website.save()
    # return JsonResponse('Payment completed!', safe=False)
    return redirect("/Error")