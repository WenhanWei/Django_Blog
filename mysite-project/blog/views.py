from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import *
import re
import markdown


# Create your views here.

def index(request):  # Home Page
    return render(request, 'blog/index.html')


def blog_index(request):
    post_list = Post.objects.order_by('-created_date')
    return render(request, 'blog/blog_index.html', context={'post_list': post_list})


"""

In the self-built MySQL database, the time zone table mysql.time_zone is empty by default,
Django configuration file Settings if USE_TZ = True,
Django USES database queries with time zones.
This results in no data being queried from MySQL.
There are two solutions:

1. Set USE_TZ=False

print(Article.objects.filter(created_time__month=5).query)
SELECT
    `blog_article`.`id`,
    `blog_article`.`title`,
    `blog_article`.`body`,
    `blog_article`.`created_time`,
    `blog_article`.`modified_time`,
    `blog_article`.`abstract`,
    `blog_article`.`category_id`,
    `blog_article`.`author_id` 
FROM
    `blog_article` 
WHERE
    EXTRACT( MONTH FROM `blog_article`.`created_time` ) = 5


# USE_TZ=True时的MySQL语句
print(Article.objects.filter(created_time__month=5).query)  
SELECT
    `blog_article`.`id`,
    `blog_article`.`title`,
    `blog_article`.`body`,
    `blog_article`.`created_time`,
    `blog_article`.`modified_time`,
    `blog_article`.`abstract`,
    `blog_article`.`category_id`,
    `blog_article`.`author_id` 
FROM
    `blog_article` 
WHERE
    EXTRACT(MONTH FROM CONVERT_TZ( `blog_article`.`created_time`, 'UTC', 'Asia/Shanghai' )) = 5

2. Import time zone data into MySQL
On Linux, execute the following command in the Shell to import the time zone into the MySQL database

$ mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root -p

"""


def blog_archive(request, year, month):
    post_list = Post.objects.filter(created_date__year=year,
                                    created_date__month=month,
                                    ).order_by('-created_date')
    return render(request, 'blog/blog_index.html', context={'post_list': post_list})


def blog_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=category).order_by('-created_date')
    return render(request, 'blog/blog_index.html', context={'post_list': post_list})


def blog_tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=tag).order_by('-created_date')
    return render(request, 'blog/blog_index.html', context={'post_list': post_list})


def blog_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Views +1
    post.increase_views()

    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    post.text = md.convert(post.text)
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''
    return render(request, 'blog/blog_detail.html', context={'post': post})


def search(request):
    q = request.GET.get('q')

    if not q:
        error_msg = "Please enter keywords"
        messages.add_message(request, messages.ERROR, error_msg, extra_tags='danger')
        return redirect('blog:index')

    post_list = Post.objects.filter(Q(title__icontains=q) | Q(text__icontains=q) | Q(text_rich__icontains=q))
    return render(request, 'blog/blog_index.html', {'post_list': post_list})


def portfolio(request):  # My Resume
    educations = Education.objects.order_by('id')
    projects = Project.objects.order_by('id')
    honors = Honor.objects.order_by('id')
    hobbies = PersonalHobby.objects.order_by('id')
    work_experiences = WorkExperience.objects.order_by('id')
    language_skills = LanguageSkill.objects.order_by('id')
    programming_skills = ProgrammingLanguageSkill.objects.order_by('id')

    return render(request,
                  'blog/portfolio.html',
                  {'educations': educations,
                   'projects': projects,
                   'honors': honors,
                   'hobbies': hobbies,
                   'work_experiences': work_experiences,
                   'language_skills': language_skills,
                   'programming_skills': programming_skills})
