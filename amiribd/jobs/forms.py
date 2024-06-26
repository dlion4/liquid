from django.shortcuts import get_object_or_404

from amiribd.users.models import Profile, User
from .models import Job, JobApplication, JobLevel, LocationTypeChoice
from django import forms
from unfold.widgets import (
     UnfoldAdminTextInputWidget,
     UnfoldAdminSelectWidget,
     UnfoldAdminDecimalFieldWidget,
     UnfoldForeignKeyRawIdWidget,
     UnfoldBooleanSwitchWidget
)
from django.contrib.admin.sites import AdminSite
from unfold.contrib.forms.widgets import ArrayWidget, WysiwygWidget


class AddJobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = "__all__"
        widgets = {
            "title": UnfoldAdminTextInputWidget(),
            "location": UnfoldAdminTextInputWidget(),
            'location_type':UnfoldAdminSelectWidget(choices=LocationTypeChoice.choices),
            "description": UnfoldAdminTextInputWidget(),
            "content":WysiwygWidget(),
            "salary_offer":UnfoldAdminDecimalFieldWidget(),
            "level":UnfoldAdminSelectWidget(choices=JobLevel.choices),
            "is_active":UnfoldBooleanSwitchWidget()
        }



class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = [
            "email_or_phone",
            "motivational_letter",
            "resume",
        ]

        widgets = {
            "email_or_phone": forms.TextInput(attrs={"class": "form-control form-control-lg", "placeholder":"Email or Phone Number"}),
            "motivational_letter": forms.Textarea(attrs={"class": "form-control form-control-lg no-resize", "rows":2}),
            "resume": forms.FileInput(attrs={"class": "form-control form-control-lg"}),
        }

        labels = {
            "email_or_phone": "Preffered Contact Channel",
            "motivational_letter": "Motivational Letter",
            "resume": "Resume",
        }

        help_text = {
            "email_or_phone": "Enter your email or phone number",
            "motivational_letter": "Write a letter of motivation to the employer",
            "resume": "Upload your resume",
        }

    def __init__(self, *args, **kwargs):
        self.job_id = kwargs.pop('job_id', None)
        self.applicant_id = kwargs.pop('applicant_id', None)
        super(JobApplicationForm, self).__init__(*args, **kwargs)

    def get_job(self):
        return get_object_or_404(Job, pk=self.job_id)
    
    def get_applicant(self):
        return get_object_or_404(Profile, pk=self.applicant_id)
    

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume:
            original_filename = resume.name

            # Check if filename length exceeds 100 characters
            if len(original_filename) > 100:
                # Split filename and extension
                filename, ext = original_filename.rsplit('.', 1)
                
                # Truncate filename to fit within 100 characters
                truncated_filename = filename[:100-len(ext)-1] + '.' + ext
                resume.name = truncated_filename

        return resume
    

    def save(self, commit=True):
        instance = super(JobApplicationForm, self).save(commit=False)
        if commit:
            instance.job = self.get_job()
            instance.applicant = self.get_applicant()
            instance.applicant.job_applications.add(
                self.get_job()
            )
            instance.applicant.save()
            instance.save()

        return instance
    


    