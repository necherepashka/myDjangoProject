from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    #old look urls -> /blog/1/
    #path('<int:id>/', views.post_detail, name='post_detail')

    #new look urls -> /blog/2023/07/10/first-post/
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', 
         views.post_detail, name='post_detail')
]