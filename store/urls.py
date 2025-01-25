from django.urls import path
from.views import create_store, add_product, store, product, delete_store, delete_product, publish, paymentComplete, \
    review_stores, review_products, accept_store, accept_product, edit_product, magic_upload, m_upload, add_category, save_product, saved_products
urlpatterns = [
    path('create/', create_store),
    path('<str:slug>/magic', m_upload),
    path('<str:slug>/magic/<path:url>/<int:category>', magic_upload),
    path('<str:slug>/', store),
    path('products/saved', saved_products),
    path('<str:slug>/categories/add', add_category),
    path('<str:slug>/products/create', add_product),
    path('<str:slug>/products/<int:id>', product),
    path('<str:slug>/products/<int:id>/delete', delete_product),
    path('<str:slug>/products/<int:id>/save', save_product),
    path('<str:slug>/products/<int:id>/edit', edit_product),
    path('<str:slug>/delete', delete_store),
    path('<str:slug>/publish', publish),
    path('publish/complete', paymentComplete, name="store_published"),
    path('review', review_stores),
    #path('<str:slug>/products/review', review_products),
    path('<str:slug>/accept', accept_store),
    #path('<str:slug>/products/<int:id>/accept', accept_product)
    ]
