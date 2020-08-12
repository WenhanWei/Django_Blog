from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [path('', views.index, name='index'),
               path('portfolio', views.portfolio, name='portfolio'),
               path('portfolio_edu_add', views.portfolio_edu_add, name='portfolio_edu_add'),
               path('portfolio_work_add', views.portfolio_work_add, name='portfolio_work_add'),
               path('portfolio_project_add', views.portfolio_project_add, name='portfolio_project_add'),
               path('portfolio_honor_add', views.portfolio_honor_add, name='portfolio_honor_add'),
               path('portfolio_language_add', views.portfolio_language_add, name='portfolio_language_add'),
               path('portfolio_programming_language_add', views.portfolio_programming_language_add,
                    name='portfolio_programming_language_add'),
               path('portfolio_hobby_add', views.portfolio_hobby_add, name='portfolio_hobby_add'),
               path('blog_index', views.blog_index, name='blog_index'),
               path('blog_detail/<int:pk>/', views.blog_detail, name='blog_detail'),
               path('blog_archives/<int:year>/<int:month>/', views.blog_archive, name='blog_archive'),
               path('blog_categories/<int:pk>/', views.blog_category, name='blog_category'),
               path('blog_tags/<int:pk>/', views.blog_tag, name='blog_tag'),
               path('search/', views.search, name='search'),
               ]
