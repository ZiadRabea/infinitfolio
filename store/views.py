import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode, urlparse, parse_qs
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .forms import *
from .models import *
from .filters import *
# Create your views here.


def store(request, slug):
    store = Store.objects.get(name=slug)
    products = Product.objects.filter(store=store)
    filter = ProductFilter(request.GET, queryset=products)
    products = filter.qs
    has_affiliate_products = products.filter(affiliate_product=True).exists()
    not_affiliate = products.filter(affiliate_product=False).exists
    if store.published or store.user == request.user.profile or request.user.is_superuser:
        context = {
            "store": store,
            "products": products,
            "filter": filter,
            "is_affiliate": has_affiliate_products,
            "not_affiliate": not_affiliate
        }
        return render(request, "store_templates/store_template2.html", context)
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
            form = AddProduct(request.POST, request.FILES, store=store)
            if form.is_valid():
                myform = form.save(commit=False)
                myform.store = store
                myform.save()
                return redirect(f"/stores/{store.name}/products/{myform.id}")
        else:
            form = AddProduct(store=store)

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
            form = AddProduct(request.POST, request.FILES, instance=product, store=store)
            if form.is_valid():
                myform = form.save(commit=False)
                myform.store = store
                myform.save()
                return redirect(f"/stores/{store.name}/products/{myform.id}")
        else:
            form = AddProduct(instance=product, store=store)

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

# @login_required
# def magic_upload(request, slug, url, category):
#     store = Store.objects.get(name=slug)
#     category = Category.objects.get(id=category)
#     if not category.store == store:
#         return redirect('/Error')
           
#     if store.user != request.user.profile:
#         return redirect("/Error")
#     else:
#         # try:
#             #Check the url : 
#             if not "https://" in url:
#                 try: 
#                     url = url.replace("https:/", "https://")
#                 except:
#                     return redirect("/Error")
#             # Send an HTTP request to the URL
#             headers = {
#                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
#                 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#                 'Accept-Encoding': 'gzip, deflate, br',
#                 'Accept-Language': 'en-US,en;q=0.9',
#                 'Connection': 'keep-alive',
#                 'Referer': url,
#             }
#             response = requests.get(url, headers=headers)
#             response.raise_for_status()  # Check for successful response (status code 200)

#             # Parse the HTML content using BeautifulSoup
#             soup = BeautifulSoup(response.content, 'html.parser')

#             # Extract product details
#             product = {}

#             # Extract the product title
#             title = soup.find('span', {'id': 'productTitle'})
#             product['title'] = title.get_text(strip=True) if title else 'Title not found'

#             # Extract the product price
#             price = soup.find('span', {'class': 'a-price-whole'})
#             product['price'] = price.get_text(strip=True) if price else None

#             # Extract the product image URL
#             img_tag = soup.find('img', {'id': 'landingImage'})
#             product['image_url'] = img_tag['src'] if img_tag else 'Image not found'

#             # Modify the URL to include the affiliate store ID
#             parsed_url = urlparse(url)
#             affiliate_link = parsed_url._replace(
#                 netloc=f"www.amazon.com",
#                 path=f"/dp/{parsed_url.path.split('/')[2]}",
#                 query=urlencode({'tag': store.amazon_affiliate_id})
#             ).geturl()

#             product['affiliate_link'] = affiliate_link

#             Product.objects.create(store=store, cover_image=None, approved=True, image_link=product["image_url"], affiliate_link=product['affiliate_link'], affiliate_product=True, name=product["title"], price=int(str(product['price']).replace(".","")), description=product['title'], cls=category)
#             return redirect(f"/stores/{store.name}")
#         # except:
#         #     return redirect('/Error')

# @login_required 
# def m_upload(request, slug):
#     store = Store.objects.get(name=slug)
#     return render(request, "magic_upload.html", {"store":store})

@login_required
def add_category(request, slug):
    store = Store.objects.get(name=slug)
    if request.user.profile == store.user:
        if request.method == "POST":
            form = AddCategory(request.POST, request.FILES)
            if form.is_valid():
                myform = form.save(commit=False)
                myform.store = store
                myform.save()
                return redirect(f"/stores/{store.name}/products/create")
        else:
            form = AddCategory()

        context = {
            "form": form
        }
        return render(request, "add_category.html", context)
    else:
        return redirect("/Error")

@login_required 
def save_product(request, slug, id):
    store = Store.objects.get(name=slug)
    product = Product.objects.get(id=id)

    if request.user.profile in product.savers.all():
        product.savers.remove(request.user.profile)
    else:
        product.savers.add(request.user.profile)

    return redirect(f"/stores/{store.name}")

@login_required
def saved_products(request):
    products = request.user.profile.savers.all()
    filter = ProductFilter(request.GET, queryset=products)
    products = filter.qs

    context = {
        "products":products
    }
    return render(request, "store_templates/saved_items.html", context=context)