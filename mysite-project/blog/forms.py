from django import forms
from django_summernote.fields import SummernoteTextFormField

from .models import *


class EducationForm(forms.ModelForm):
    details_of_education = SummernoteTextFormField()

    class Meta:
        model = Education
        fields = ['name_of_education', 'start_date_of_education', 'end_date_of_education', 'details_of_education']


class WorkExperienceForm(forms.ModelForm):
    details_of_work_and_internship = SummernoteTextFormField()

    class Meta:
        model = WorkExperience
        fields = ['name_of_work_and_internship', 'job_title', 'start_date_of_work_and_internship',
                  'end_date_of_work_and_internship', 'details_of_work_and_internship']


class ProjectForm(forms.ModelForm):
    details_of_project_experience = SummernoteTextFormField()

    class Meta:
        model = Project
        fields = ['name_of_project_experience', 'project_job_title', 'start_date_of_project_experience',
                  'end_date_of_project_experience', 'details_of_project_experience']


class LanguageForm(forms.ModelForm):
    class Meta:
        model = LanguageSkill
        fields = ['language_skills']


class ProgrammingLanguageForm(forms.ModelForm):
    programming_language_skill_details = SummernoteTextFormField()

    class Meta:
        model = ProgrammingLanguageSkill
        fields = ['programming_language_skill', 'programming_language_skill_details']


class HonorForm(forms.ModelForm):
    class Meta:
        model = Honor
        fields = ['name_of_the_honor']


class PersonalHobbyForm(forms.ModelForm):
    class Meta:
        model = PersonalHobby
        fields = ['personal_hobby']
