from django.urls import reverse
from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from amiribd.users.models import Profile
from django_extensions.db.fields import AutoSlugField
from amiribd.articles.models import my_slugify_function
from django.core.exceptions import ValidationError


class JobQuerySet(models.QuerySet):
    def online_jobs(self):
        return self.filter(location_type__iexact="Online")
    
    def physical_jobs(self):
        return self.filter(location_type__iexact="Physical")
    
    def abroad_jobs(self):
        return self.filter(location_type__iexact="Abroad")

class JobManager(models.Manager):

    def online_jobs(self):
        return self.filter(location_type__iexact="Online")

    def physical_jobs(self):
        return self.filter(location_type__iexact="Physical")

    def abroad_jobs(self):
        return self.filter(location_type__iexact="Abroad")
    
class LocationTypeChoice(models.TextChoices):
    Online = "Online", "Online"
    Physical = "Physical", "Physical"
    Abroad = "Abroad", "Abroad"
    

class JobLevel(models.TextChoices):
    A = "A", "Career"
    B = "B", "Manual"
    I = "I","Freelance"

# Create your models here.
class Job(models.Model):
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from="title", slugify_function=my_slugify_function)
    location = models.CharField(max_length=255, help_text="online, Nairobi, Qatar, etc")
    location_type = models.CharField(
        max_length=20, help_text="Online, Physical, Abroad, etc", choices=LocationTypeChoice.choices, default=LocationTypeChoice.Online)
    description = models.TextField(max_length=1000)
    content = models.TextField()
    salary_offer = models.DecimalField(max_digits=12, decimal_places=2, default=10.89)
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        Profile, verbose_name=_("Job Author"), on_delete=models.SET_NULL, null=True, blank=True
    )
    job_file = models.FileField(blank=True, null=True, upload_to="jobs/instructions/")
    level = models.CharField(choices=JobLevel.choices, default=JobLevel.B, max_length=1)
    is_active = models.BooleanField(default=True)
    resume_required = models.BooleanField(default=False, help_text="This is to show whether the applicant should attach resume letter a long the application")
    motivation_letter_required = models.BooleanField(default=False, help_text="This is to show whether the applicant should attach motivational letter a long the application")
    bidding_offer_required = models.BooleanField(default=False, help_text="This is to show whether the applicant should place his biding while applying")
    is_completed = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)

    objects = JobManager()
    
    class Meta:
        ordering = ["-id"]


    @property
    def is_popular(self):
        return self.job_applications >= 1000
    
    @property
    def job_applications(self):
        return self.applications.count()
    
    @property
    def is_new(self):
        return self.date_posted <= timezone.now() - timezone.timedelta(days=30)
    

    def __str__(self):
        return self.title
    

def upload_application_resume(instance, filename):
    return f"applications/aplicant-{instance.applicant.pk}/{instance.job.pk}/application/{timezone.now().year}/{timezone.now().month}/{timezone.now().day}/{filename}"
    
class ApplicationStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    ACCEPTED = "ACCEPTED", "Accepted"
    REJECTED = "REJECTED", "Rejected"
    CANCELLED = "CANCELLED","Cancelled"


class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile_job_applications")
    motivational_letter = models.TextField(blank=True, null=True)
    bidding_offer = models.TextField(blank=True, null=True)
    email_or_phone = models.CharField(max_length=100, blank=True, null=True)
    resume = models.FileField(upload_to=upload_application_resume, blank=True, null=True)
    status = models.CharField(choices=ApplicationStatus.choices, max_length=10, default=ApplicationStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Application for Job Id: {self.job.pk}"
    
    class Meta:
        get_latest_by = "created_at"
        ordering = ['-created_at']
    

    def get_cancel_url(self):
        return reverse("dashboard:invest:jobs:job_cancel_job_application", kwargs={
            "application_id": self.pk,
        })
    def get_reactivation_url(self):
        return reverse("dashboard:invest:jobs:job_reactivate_job_application", kwargs={
            "application_id": self.pk,
        })


class JobApplicationSubmission(models.Model):
    job_application = models.ForeignKey(
        Job, on_delete=models.CASCADE, related_name="jobs_submissions")
    uploader = models.ForeignKey(Profile,
                                 null=True,
                                 blank=True, related_name="submitted_by",
                                 on_delete=models.SET_NULL)
    submission_date = models.DateTimeField(auto_now_add=True)
    submission_file = models.FileField(upload_to="submissions/")
    approved = models.BooleanField(default=False)

    def __str__(self):
        return str(self.uploader.first_name)

    def clean(self):
        if self.job_application.location_type != "Online":
            msg = "You can only submit an application for online jobs."
            raise ValidationError(msg)

    class Meta:  # noqa: DJ012
        verbose_name = "Job Application Submission"
        verbose_name_plural = "Job Application Submissions"
