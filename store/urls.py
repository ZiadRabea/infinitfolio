from django.urls import path
from.views import *
urlpatterns = [
    path('create/', create_store),
    path('api/store-views-data', store_views_data),
    # path('<str:slug>/magic/<path:url>/<int:category>', magic_upload),
    path('<str:slug>/', store),
    path('<str:slug>/templates', select_temp),
    path('<str:slug>/templates/<int:id>/select', select),
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
