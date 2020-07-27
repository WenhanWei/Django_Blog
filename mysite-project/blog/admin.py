from django.contrib import admin
from .models import *

from django_summernote.admin import SummernoteModelAdmin
from .models import Post, Education


# Apply summernote to selected TextField in model.
class PostAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = ('text_rich',)


# Apply summernote to all TextField in model.
class EducationAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = '__all__'


class WorkExperienceAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = '__all__'


class ProjectAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = '__all__'


class ProgrammingLanguageSkillAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = '__all__'


# Register your models here.
# admin.site.register(Education)

admin.site.register(Education, EducationAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(WorkExperience, WorkExperienceAdmin)

admin.site.register(Honor)
admin.site.register(LanguageSkill)
admin.site.register(ProgrammingLanguageSkill, ProgrammingLanguageSkillAdmin)
admin.site.register(PersonalHobby)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(Category)
