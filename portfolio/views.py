from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import *
import json
# Create your views here.


def home(request):
    return render(request, "index.html")


def error(request):
    return render(request, "error.html")


@login_required
def create(request):
    if request.method == "POST":
        form = CreateWebsite(request.POST, request.FILES)
        if form.errors:
            print(form.errors)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.user = request.user.profile
            myform.save()
            website = Website.objects.get(id=myform.id)
            certs = request.FILES.getlist("certificates")
            for i in certs:
                Certificate.objects.create(cert=i, website=website)
            for i in range(4):
                skill = request.POST[f"skill{i+1}"]
                mastery = request.POST[f"mastery{i+1}"]
                Skill.objects.create(skill=skill, mastery=mastery, website=website)
            project = request.POST["project1T"]
            about_project = request.POST["Project1"]
            Project.objects.create(title=project, about=about_project, website=website)

            work = request.POST["work1T"]
            years = request.POST["work1Y"]
            about_work = request.POST["work1"]
            Experience.objects.create(job=work, years=years, about=about_work, website=website)

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
