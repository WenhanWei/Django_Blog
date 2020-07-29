import markdown
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.html import strip_tags

# Create your models here.

"""
django 内置的全部类型可查看文档：
https://docs.djangoproject.com/en/2.2/ref/models/fields/#field-types
ForeignKey、ManyToManyField 不了解，可参考官方文档：
https://docs.djangoproject.com/en/2.2/topics/db/models/#relationships
"""


class Education(models.Model):
    name_of_education = models.CharField(max_length=100)
    start_date_of_education = models.DateField(blank=True, null=True)
    end_date_of_education = models.DateField(blank=True, null=True)
    details_of_education = models.TextField()

    def __str__(self):
        return self.name_of_education


class WorkExperience(models.Model):
    name_of_work_and_internship = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    start_date_of_work_and_internship = models.DateField(blank=True, null=True)
    end_date_of_work_and_internship = models.DateField(blank=True, null=True)
    details_of_work_and_internship = models.TextField()

    def __str__(self):
        return self.name_of_work_and_internship


class Project(models.Model):
    name_of_project_experience = models.CharField(max_length=100)
    project_job_title = models.CharField(max_length=100)
    start_date_of_project_experience = models.DateField(blank=True, null=True)
    end_date_of_project_experience = models.DateField(blank=True, null=True)
    details_of_project_experience = models.TextField()

    def __str__(self):
        return self.name_of_project_experience


class LanguageSkill(models.Model):
    language_skills = models.CharField(max_length=100)

    def __str__(self):
        return self.language_skills


class ProgrammingLanguageSkill(models.Model):
    programming_language_skill = models.CharField(max_length=100)
    programming_language_skill_details = models.TextField()

    def __str__(self):
        return self.programming_language_skill


class Honor(models.Model):
    name_of_the_honor = models.CharField(max_length=200)

    def __str__(self):
        return self.name_of_the_honor


class PersonalHobby(models.Model):
    personal_hobby = models.CharField(max_length=100)

    def __str__(self):
        return self.personal_hobby


class Category(models.Model):
    """
    Category of my blog
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    Blog Tag
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    Blog post database
    """

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=70)
    abstract = models.CharField(max_length=200, blank=True)
    text = models.TextField(blank=True)
    text_rich = models.TextField(blank=True)
    views = models.PositiveIntegerField(default=0, editable=False)

    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        ordering = ['-created_date', 'title']

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse('blog:blog_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if self.abstract:
            self.modified_date = timezone.now()
            super().save(*args, **kwargs)
        else:
            self.modified_date = timezone.now()

            # First instantiates a Markdown class that renders the text of the text.
            # Since abstracts do not need to generate article directories, directory extensions are removed.
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])

            # First render the Markdown text as HTML text
            # strip_tags Strip out all HTML tags of HTML text
            # then give 54 chars to abstract
            if self.text:
                self.abstract = strip_tags(md.convert(self.text))[:50]
            else:
                self.abstract = strip_tags(md.convert(self.text_rich))[:50]

            super().save(*args, **kwargs)

    def __str__(self):
        return self.title
