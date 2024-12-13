from django.urls import path
from.views import create_store, add_product, store, product, delete_store, delete_product, publish, paymentComplete, \
    review_stores, review_products, accept_store, accept_product, edit_product
urlpatterns = [
    path('create/', create_store),
    path('<str:slug>/', store),
    path('<str:slug>/products/create', add_product),
    path('<str:slug>/products/<int:id>', product),
    path('<str:slug>/products/<int:id>/delete', delete_product),
    path('<str:slug>/products/<int:id>/edit', edit_product),
    path('<str:slug>/delete', delete_store),
    path('<str:slug>/publish', publish),
    path('publish/complete', paymentComplete, name="store_published"),
    path('review', review_stores),
    #path('<str:slug>/products/review', review_products),
    path('<str:slug>/accept', accept_store),
    #path('<str:slug>/products/<int:id>/accept', accept_product)
    ]
