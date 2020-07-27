from django.contrib import admin
from .models import Comment


# Register your models here.

class CommentAdmin(admin.ModelAdmin):
    fields = ['name', 'email', 'text', 'post']


admin.site.register(Comment, CommentAdmin)
