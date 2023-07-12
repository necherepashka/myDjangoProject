from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    #base on function
    #path('', views.post_list, name='post_list'),

    #base on class
    #path('', views.PostListView.as_view(), name='post_list'),

    #old look urls -> /blog/1/
    #path('<int:id>/', views.post_detail, name='post_detail')

    #new look urls -> /blog/2023/07/10/first-post/
    #path('<int:year>/<int:month>/<int:day>/<slug:post>/', 
    #     views.post_detail, name='post_detail'),
    #path('<int:post_id>/share/', views.post_share, name='post_share'),
    #path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail,
         name='post_detail'),
    path('<int:post_id>/share/',
         views.post_share, name='post_share'),
    path('<int:post_id>/comment/',
         views.post_comment, name='post_comment'),
]