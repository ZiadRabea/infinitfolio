from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
import json
from .models import Menu, MenuProduct, QrRequest
from.forms import MProduct
# Create your views here.


@login_required
def create_menu(request):
    return render(request, "create_menu.html")


def menu(request, id):
    menu = Menu.objects.get(id=id)
    context = {
        "menu": menu
    }
    return render(request, "menu.html", context)


def user_menus(request):
    menus = Menu.objects.filter(user=request.user.profile)
    context = {
        "menus": menus
    }
    return render(request, "requests.html", context)


@login_required
def create_item(request, id):
    menu = Menu.objects.get(id=id)
    if menu.user == request.user.profile:
        if request.method == "POST":
            form = MProduct(request.POST, request.FILES)
            if form.is_valid():
                my_form = form.save(commit=False)
                my_form.menu = menu
                my_form.save()
                return redirect(f"/menus/{menu.id}")
        else:
            form = MProduct()
        context = {
            "form": form
        }
        return render(request, "add_menu_item.html", context)
    else:
        return redirect("/Error")

@login_required
def edit_item(request, id, pid):
    menu = Menu.objects.get(id=id)
    if menu.user == request.user.profile:
        product = MenuProduct.objects.get(id=pid)
        if request.method == "POST":
            form = MProduct(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                return redirect(f"/menus/{menu.id}")
        else:
            form = MProduct(instance=product)
        context = {
            "form": form
        }
        return render(request, "add_menu_item.html", context)
    else:
        return redirect("/Error")

@login_required
def review_requests(request):
    if request.user.is_superuser:
        r = QrRequest.objects.all()
        context = {
            "requests": r
        }
        return render(request, "requests.html", context)
    else:
        return redirect("/Error")


@login_required
def mark_review(request, id):
    if request.user.is_superuser:
        qrr = QrRequest.objects.get(id=id)
        qrr.done = True
        qrr.save()
        return redirect("menu/requests")
    else:
        return redirect("/Error")


@login_required
def paymentComplete(request):
    menu = Menu.objects.create(user=request.user.profile)
    QrRequest.objects.create(menu=menu, user=request.user.profile)
    response_data = {
        'message': 'Payment completed!',
        'status': 'success',
        'menu_id': menu.id
    }

    return JsonResponse(response_data, safe=False)
