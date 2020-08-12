import re

import markdown
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from .forms import EducationForm, WorkExperienceForm, ProjectForm, LanguageForm, ProgrammingLanguageForm, HonorForm, \
    PersonalHobbyForm
from .models import *


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

    context = {'educations': educations,
               'projects': projects,
               'honors': honors,
               'hobbies': hobbies,
               'work_experiences': work_experiences,
               'language_skills': language_skills,
               'programming_skills': programming_skills}

    return render(request, 'blog/portfolio.html', context=context)


def portfolio_edu_add(request):
    if request.method == 'POST':
        education_form = EducationForm(request.POST)

        if education_form.is_valid():
            education_form.save()
            return HttpResponseRedirect('/portfolio')

    education_form = EducationForm()

    context = {
        'education_form': education_form,
    }

    return render(request, 'blog/portfolio_edu_add.html', context=context)


def portfolio_work_add(request):
    if request.method == 'POST':
        work_form = WorkExperienceForm(request.POST)

        if work_form.is_valid():
            work_form.save()
            return HttpResponseRedirect('/portfolio')

    work_form = WorkExperienceForm()
    context = {
        'work_form': work_form,
    }

    return render(request, 'blog/portfolio_work_add.html', context=context)


def portfolio_project_add(request):
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)

        if project_form.is_valid():
            project_form.save()
            return HttpResponseRedirect('/portfolio')

    project_form = ProjectForm()
    context = {
        'project_form': project_form,
    }

    return render(request, 'blog/portfolio_project_add.html', context=context)


def portfolio_language_add(request):
    if request.method == 'POST':
        language_form = LanguageForm(request.POST)

        if language_form.is_valid():
            language_form.save()
            return HttpResponseRedirect('/portfolio')

    language_form = LanguageForm()
    context = {
        'language_form': language_form,
    }

    return render(request, 'blog/portfolio_language_add.html', context=context)


def portfolio_programming_language_add(request):
    if request.method == 'POST':
        programming_language_form = ProgrammingLanguageForm(request.POST)

        if programming_language_form.is_valid():
            programming_language_form.save()
            return HttpResponseRedirect('/portfolio')

    programming_language_form = ProgrammingLanguageForm()
    context = {
        'programming_language_form': programming_language_form,
    }

    return render(request, 'blog/portfolio_programming_language_add.html', context=context)


def portfolio_honor_add(request):
    if request.method == 'POST':
        honor_form = HonorForm(request.POST)

        if honor_form.is_valid():
            honor_form.save()
            return HttpResponseRedirect('/portfolio')

    honor_form = HonorForm()
    context = {
        'honor_form': honor_form,
    }

    return render(request, 'blog/portfolio_honor_add.html', context=context)


def portfolio_hobby_add(request):
    if request.method == 'POST':
        personal_hobby_form = PersonalHobbyForm(request.POST)

        if personal_hobby_form.is_valid():
            personal_hobby_form.save()
            return HttpResponseRedirect('/portfolio')

    personal_hobby_form = PersonalHobbyForm()
    context = {
        'personal_hobby_form': personal_hobby_form
    }

    return render(request, 'blog/portfolio_hobby_add.html', context=context)
