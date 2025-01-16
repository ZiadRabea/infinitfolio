import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .forms import *
from .models import *
from .filters import *
# Create your views here.


def store(request, slug):
    store = Store.objects.get(name=slug)
    products = Product.objects.filter(store=store, affiliate_product=False)
    affiliate_products = Product.objects.filter(store=store, affiliate_product=True)
    filter = ProductFilter(request.GET, queryset=products)
    products = filter.qs
    if store.published or store.user == request.user.profile or request.user.is_superuser:
        context = {
            "store": store,
            "products": products,
            "affiliate_products": affiliate_products,
            "filter": filter
        }
        return render(request, "store.html", context)
    else:
        return redirect("/Error")


def product(request, slug, id):
    store = Store.objects.get(name=slug)
    product = Product.objects.get(id=id)
    profile = request.user.profile if request.user.is_authenticated else None
    if product.store.user == profile or product.store.published or request.user.is_superuser:
        context = {
            "store": store,
            "product": product
        }
        return render(request, "e-shop.html", context)
    else:
        return redirect("/Error")


@login_required
def create_store(request):
    if request.method == "POST":
        form = CreateStore(request.POST, request.FILES)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.user = request.user.profile
            myform.save()
            return redirect(f"/stores/{myform.name}")
    else:
        form = CreateStore()

    context = {
        "form": form
    }
    return render(request, "create_store.html", context)


@login_required
def delete_store(request, slug):
    store = Store.objects.get(name=slug)
    if store.user == request.user.profile:
        store.delete()
        return redirect("/")
    else:
        return redirect("/Error")


@login_required
def add_product(request, slug):
    store = Store.objects.get(name=slug)
    if store.user == request.user.profile:
        if request.method == "POST":
            form = AddProduct(request.POST, request.FILES)
            if form.is_valid():
                myform = form.save(commit=False)
                myform.store = store
                myform.save()
                return redirect(f"/stores/{store.name}/products/{myform.id}")
        else:
            form = AddProduct()

        context = {
            "form": form,
            "store": store
        }
        return render(request, "add_product.html", context)
    else:
        return redirect("/Error")

@login_required
def edit_product(request, slug, id):
    store = Store.objects.get(name=slug)
    product = Product.objects.get(id=id)
    if not product.store == store: 
        return redirect("/Error")
    if store.user == request.user.profile:
        if request.method == "POST":
            form = AddProduct(request.POST, request.FILES, instance=product)
            if form.is_valid():
                myform = form.save(commit=False)
                myform.store = store
                myform.save()
                return redirect(f"/stores/{store.name}/products/{myform.id}")
        else:
            form = AddProduct(instance=product)

        context = {
            "form": form,
            "store": store
        }
        return render(request, "add_product.html", context)
    else:
        return redirect("/Error")

@login_required
def delete_product(request, slug, id):
    store = Store.objects.get(name=slug)
    product = Product.objects.get(id=id)
    if store.user == request.user.profile:
        product.delete()
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
    # print(website_unique_name)
    # website = Store.objects.get(name=website_unique_name)
    # print(website.name)
    # website.published = True
    # website.save()
    # return JsonResponse('Payment completed!', safe=False)
    return redirect("/Error")

@login_required
def review_stores(request):
    if request.user.is_superuser:
        stores = Store.objects.filter(approved=False)
        context = {
            "stores": stores
        }
        return render(request, "review_stores.html", context)
    else:
        return redirect("/Error")


@login_required
def review_products(request, store, id):
    if request.user.is_superuser:
        products = Product.objects.filter(approved=False)
        context = {
            "products": products
        }
        return render(request, "review_products.html", context)
    else:
        return redirect("/Error")


@login_required
def accept_store(request, slug):
    if request.user.is_superuser:
        store = Store.objects.get(name=slug)
        store.approved = True
        store.save()
        return redirect(f"/stores/review")
    else:
         return redirect("/Error")


@login_required
def accept_product(request, slug, id):
    if request.user.is_superuser:
        product = Product.objects.get(id=id)
        product.approved = True
        product.save()
    else:
        return redirect("/Error")
