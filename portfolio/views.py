from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import *
from .filters import *
import json
# Create your views here.


def home(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 5)
    try: 
        store = request.user.profile.store
    except:
        store = None
    try: 
        blog = request.user.profile.blog
    except:
        blog = None
    try:
        website = request.user.profile.website
    except:
        website = None
    
    if request.user.is_authenticated and not website:
        return redirect("/create")
    
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(receiver=request.user.profile.website, read=False)
    else:
        notifications = ""
    if request.method == "POST":
        #print(bool(request.POST["text"]), bool(request.FILES["image"]))
        try: 
            profile = Website.objects.get(user=request.user.profile)
            form = CreateCommnunityPost(request.POST, request.FILES)
            
            if not (bool(request.POST["text"]) or bool(request.FILES["image"])):
                    return redirect("/Error")
            else:
                if form.is_valid():
                    myform = form.save(commit=False)
                    myform.profile = profile
                    myform.save()
                    return redirect("/")
        except Exception:
            return redirect('/create')
    else:
        form = CreateCommnunityPost()
    
    context = {
        "posts": page_obj,
        "form": form,
        "store": store,
        "blog": blog,
        "notifications": notifications
    }
    return render(request, "index.html", context)


def organiser(request):
    return render(request, "mylife.html")


def error(request):
    return render(request, "error.html")

def search(request):
    cvs = Website.objects.filter(is_active=True)
    filter = WebsiteFilter(request.GET, queryset = cvs)
    cvs = filter.qs

    context = {
        "cvs" : cvs,
        "filter": filter
    }
    return render(request, "search.html", context)

@login_required
def create(request):
    try:
        website = request.user.profile.website
    except Exception:
        website = None
    if website : return redirect("/") 
    if request.method == "POST":
        form = CreateWebsite(request.POST, request.FILES)
        if form.errors:
            print(form.errors)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.user = request.user.profile
            myform.is_active = True
            myform.save()
            website = Website.objects.get(id=myform.id)
            # certs = request.FILES.getlist("certificates")

            # if certs:
            #     for i in certs:
            #         Certificate.objects.create(cert=i, website=website)
            #     for i in range(4):
            #         skill = request.POST[f"skill{i+1}"]
            #         mastery = request.POST[f"mastery{i+1}"]
            #         if skill and mastery:
            #             Skill.objects.create(skill=skill, mastery=mastery, website=website)
            # project = request.POST["project1T"]
            # about_project = request.POST["Project1"]
            # if project and about_project:
            #     Project.objects.create(title=project, about=about_project, website=website)

            # work = request.POST["work1T"]
            # years = request.POST["work1Y"]
            # about_work = request.POST["work1"]
            # if work and years and about_work:
            #     Experience.objects.create(job=work, years=years, about=about_work, website=website)

            return redirect(f"/{website.unique_name}")

    else:
        form = CreateWebsite()

    context = {
        "form": form
    }

    return render(request, "create.html", context)


def display(request, slug):
    website = Website.objects.get(unique_name=slug)
    skills = Skill.objects.filter(website=website)
    projects = Project.objects.filter(website=website)
    work = Experience.objects.filter(website=website)
    certs = Certificate.objects.filter(website=website)
    context = {
        "website": website,
        "skills": skills,
        "projects": projects,
        "works": work,
        "certs": certs
    }
    return render(request, "website.html", context)


@login_required
def add_skill(request, slug):
    website = Website.objects.get(unique_name=slug)
    if request.user.profile != website.user:
        return redirect("/Error")
    else:
        skills = Skill.objects.filter(website=website)
        if request.method == "POST":
            form = AddSkill(request.POST)
            if form.is_valid():
                myform = form.save(commit=False)
                myform.website = website
                myform.save()
                return redirect(f"/{website.unique_name}")
        else:
            form = AddSkill()
        context = {
            "website": website,
            "form": form,
            "skills": skills
        }
        return render(request, "add_skill.html", context)


@login_required
def delete_skill(request, id):
    skill = Skill.objects.get(id=id)
    if request.user.profile == skill.website.user:
        website_slug = skill.website.unique_name
        skill.delete()
        return redirect(f"/{website_slug}")
    else:
        return redirect("/Error")


@login_required
def add_certificate(request, slug):
    website = Website.objects.get(unique_name=slug)
    if request.user.profile != website.user:
        return redirect("/Error")
    else:
        certs = Certificate.objects.filter(website=website)
        if request.method == "POST":
            form = AddCertificate(request.POST, request.FILES)
            if form.is_valid():
                myform = form.save(commit=False)
                myform.website = website
                myform.save()
                return redirect(f"/{website.unique_name}")
        else:
            form = AddCertificate()
        context = {
            "website": website,
            "form": form,
            "certs": certs
        }
        return render(request, "certificates.html", context)


@login_required
def delete_certificate(request, id):
    cert = Certificate.objects.get(id=id)
    if request.user.profile == cert.website.user:
        website_slug = cert.website.unique_name
        cert.delete()
        return redirect(f"/{website_slug}")
    else:
        return redirect("/Error")


@login_required
def add_project(request, slug):
    website = Website.objects.get(unique_name=slug)
    if request.user.profile != website.user:
        return redirect("/Error")
    else:
        projects = Project.objects.filter(website=website)
        if request.method == "POST":
            form = AddProject(request.POST, request.FILES)
            if form.is_valid():
                myform = form.save(commit=False)
                myform.website = website
                myform.save()
                return redirect(f"/{website.unique_name}")
        else:
            form = AddProject()
        context = {
            "website": website,
            "form": form,
            "projects": projects
        }
        return render(request, "projects.html", context)


@login_required
def delete_project(request, id):
    project = Project.objects.get(id=id)
    if request.user.profile == project.website.user:
        website_slug = project.website.unique_name
        project.delete()
        return redirect(f"/{website_slug}")
    else:
        return redirect("/Error")


@login_required
def add_work(request, slug):
    website = Website.objects.get(unique_name=slug)
    if request.user.profile != website.user:
        return redirect("/Error")
    else:
        work = Experience.objects.filter(website=website)
        if request.method == "POST":
            form = AddExperience(request.POST, request.FILES)
            if form.is_valid():
                myform = form.save(commit=False)
                myform.website = website
                myform.save()
                return redirect(f"/{website.unique_name}")
        else:
            form = AddExperience()
        context = {
            "website": website,
            "form": form,
            "work": work
        }
        return render(request, "work_experience.html", context)


@login_required
def delete_work(request, id):
    work = Experience.objects.get(id=id)
    if request.user.profile == work.website.user:
        website_slug = work.website.unique_name
        work.delete()
        return redirect(f"/{website_slug}")
    else:
        return redirect("/Error")


@login_required
def edit_info(request, slug):
    website = Website.objects.get(unique_name=slug)
    if request.user.profile == website.user:
        if request.method == "POST":
            form = EditWebsite(request.POST, request.FILES, instance=website)
            if form.errors:
                print(form.errors)
            if form.is_valid():
                myform = form.save(commit=False)
                myform.id = website.id
                myform.user = request.user.profile
                myform.save()
                return redirect(f"/{website.unique_name}")
        else:
            form = CreateWebsite(instance=website)
        context = {
            "website": website,
            "form": form
        }
        return render(request, "edit.html", context)
    else:
        return redirect("/Error")


def delete_website(request, slug):
    website = Website.objects.get(unique_name=slug)
    if request.user.profile == website.user:
        website.delete()
        return redirect("/")
    else:
        return redirect("/Error")


@login_required
def publish(request, slug):
    return redirect("/Error")


@login_required
def paymentComplete(request):
    # print('REQUEST BODY:', request.body)
    # body = json.loads(request.body)
    # print('BODY:', body)
    # website_unique_name = body['site_name']

    # website = Website.objects.get(unique_name=website_unique_name)
    # print(website.cv_url)
    # website.is_active = True
    # website.save()
    # return JsonResponse('Payment completed!', safe=False)
    return redirect("/Error")

@login_required
def publish_virtual(request, slug):
    website = Website.objects.get(unique_name=slug)
    user = request.user.profile
    if website.user != user:
        print("you don't own this website")
        return redirect("/Error")
    if user.coins >= .5:
        website.is_active = True
        website.save()
        user.coins = user.coins - 0.5
        user.save()
        return redirect(f"/{website.unique_name}")
    else:
        print("you don't have enough credits")
        return redirect("/Error")

@login_required
def like(request, id):
    post = Post.objects.get(id=id)
    if request.user.profile.website in post.likes.all():
        post.likes.remove(request.user.profile.website)
    else:
        post.likes.add(request.user.profile.website)
        Notification.objects.create(receiver=post.profile, sender=request.user.profile.website, content=f"liked your post : {str(post)}", url=f"/posts/{post.id}")
    return redirect(f"/posts/{id}")

@login_required
def dislike(request, id):
    post = Post.objects.get(id=id)
    if request.user.profile.website in post.dislikes.all():
        post.dislikes.remove(request.user.profile.website)
    else:
        post.dislikes.add(request.user.profile.website)
    return redirect(f"/posts/{id}")

@login_required
def post(request, id):
    post = Post.objects.get(id=id)
    try: 
        store = request.user.profile.store
    except:
        store = None
    try: 
        blog = request.user.profile.blog
    except:
        blog = None
    notifications = Notification.objects.filter(receiver=request.user.profile.website, read=False)
    paginator = Paginator(post.comment_set.all(), 2)
    page_number = request.GET.get("page")
    comments = paginator.get_page(page_number)
    if request.method == "POST":
        try: 
            profile = Website.objects.get(user=request.user.profile)
            form = AddComment(request.POST, request.FILES)
            if form.is_valid():
                myform = form.save(commit=False)
                myform.profile = profile
                myform.post = post
                myform.save()
                if request.user.profile.website == post.profile:
                    pass
                else:
                    Notification.objects.create(receiver=post.profile, sender=request.user.profile.website, content=f"has commented on your post : {myform.text}", url=f"/posts/{post.id}")
                return redirect(f"/posts/{post.id}")
        except Exception:
            return redirect('/create')
    else:
        form = AddComment()
    
    context = {
        "post": post,
        "form": form,
        "store":store,
        "blog": blog,
        "notifications": notifications,
        "comments": comments
    }
    return render(request, "postpage.html", context)

@login_required
def like_comment(request, id):
    comment = Comment.objects.get(id=id)
    if request.user.profile.website in comment.likes.all():
        comment.likes.remove(request.user.profile.website)
    else:
        comment.likes.add(request.user.profile.website)
        Notification.objects.create(receiver=comment.profile, sender=request.user.profile.website, content=f"liked your comment : {str(comment)}", url=f"/posts/{comment.post.id}")
    return redirect(f"/posts/{comment.post.id}")

@login_required
def dislike_comment(request, id):
    comment = Comment.objects.get(id=id)
    if request.user.profile.website in comment.dislikes.all():
        comment.dislikes.remove(request.user.profile.website)
    else:
        comment.dislikes.add(request.user.profile.website)
    return redirect(f"/posts/{comment.post.id}")

@login_required
def repost():
    pass

@login_required
def delete_post(request, id):
    post = Post.objects.get(id=id)
    if request.user.profile.website == post.profile:
        post.delete()
        return redirect("/")
    else:
        return redirect("/Error")
    
@login_required
def edit_post(request, id):
    post = Post.objects.get(id=id)
    if request.user.profile.website == post.profile:
        if request.method == "POST":
            form = CreateCommnunityPost(request.POST, request.FILES, instance=post)
            if form.is_valid:
                form.save()
                return redirect(f"/posts/{post.id}")
        else:
            form = CreateCommnunityPost(instance=post)
        
        context = {
            "post": post,
            "form": form
        }
        return render(request, "edit-post.html", context)
    else:
        return redirect("/Error")

@login_required
def delete_comment(request, id):
    comment = Comment.objects.get(id=id)
    if request.user.profile.website == comment.profile:
        comment.delete()
        return redirect(f"/posts/{comment.post.id}")
    else:
        return redirect("/Error")

@login_required
def edit_comment(request, id):
    comment = Comment.objects.get(id=id)
    notifications = Notification.objects.filter(receiver=request.user.profile.website, read=False)
    paginator = Paginator(comment.post.comment_set.all(), 2)
    page_number = request.GET.get("page")
    comments = paginator.get_page(page_number)
    if request.user.profile.website == comment.profile:
        if request.method == "POST":
            form = AddComment(request.POST, request.FILES, instance=comment)
            if form.is_valid:
                form.save()
                return redirect(f"/posts/{comment.post.id}")
        else:
            form = AddComment(instance=comment)
        
        context = {
            "post": comment.post,
            "form": form,
            "comments":comments,
            "notifications": notifications
        }
        return render(request, "postpage.html", context)
    else:
        return redirect("/Error")

@login_required
def notifications(request):
    notifications = Notification.objects.filter(receiver=request.user.profile.website)
    notifications.update(read=True)
    paginator = Paginator(notifications, 8)
    page_number = request.GET.get("page")
    notifications = paginator.get_page(page_number)
    return render(request, "notifications.html", {"notifications": notifications})