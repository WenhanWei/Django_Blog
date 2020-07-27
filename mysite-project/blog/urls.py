from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [path('', views.index, name='index'),
               path('portfolio', views.portfolio, name='portfolio'),
               path('blog_index', views.blog_index, name='blog_index'),
               path('blog_detail/<int:pk>/', views.blog_detail, name='blog_detail'),
               path('blog_archives/<int:year>/<int:month>/', views.blog_archive, name='blog_archive'),
               path('blog_categories/<int:pk>/', views.blog_category, name='blog_category'),
               path('blog_tags/<int:pk>/', views.blog_tag, name='blog_tag'),
               path('search/', views.search, name='search'),
               ]
