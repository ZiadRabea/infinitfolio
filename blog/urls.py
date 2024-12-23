from django.urls import path
from.views import create_blog, blog, add_post, post, add_heading, add_paragraph, add_link, add_image, add_line, \
    add_frame, add_list, add_item, publish_post, delete_post, delete_blog, publish, paymentComplete, add_topic, blogs, posts
urlpatterns = [
    path('', blogs),
    path('create/', create_blog),
    path('posts/', posts),
    path('<str:slug>/', blog),
    path('<str:slug>/posts/create', add_post),
    path('<str:slug>/topics/create', add_topic),
    path('<str:slug>/posts/<int:id>', post),
    path('<str:slug>/posts/<int:id>/addHeading', add_heading),
    path('<str:slug>/posts/<int:id>/addParagraph', add_paragraph),
    path('<str:slug>/posts/<int:id>/addLink', add_link),
    path('<str:slug>/posts/<int:id>/addImage', add_image),
    path('<str:slug>/posts/<int:id>/addFrame', add_frame),
    path('<str:slug>/posts/<int:id>/addLine', add_line),
    path('<str:slug>/posts/<int:id>/addList', add_list),
    path('<str:slug>/posts/<int:id>/list/<int:lid>/addItem', add_item),
    path('<str:slug>/posts/<int:id>/publish', publish_post),
    path('<str:slug>/posts/<int:id>/delete', delete_post),
    path('<str:slug>/delete', delete_blog),
    path('<str:slug>/publish', publish),
    path('publish/complete', paymentComplete, name="plog_published")
    ]