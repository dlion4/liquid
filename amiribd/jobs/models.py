from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from amiribd.users.models import Profile
from django_extensions.db.fields import AutoSlugField
from amiribd.articles.models import my_slugify_function


class JobQuerySet(models.QuerySet):
    def online_jobs(self):
        return self.filter(location_type__iexact="Online")
    
    def physical_jobs(self):
        return self.filter(location_type__iexact="Physical")
    
    def abroad_jobs(self):
        return self.filter(location_type__iexact="Abroad")

class JobManager(models.Manager):
    def get_queryset(self):
        return JobQuerySet(self.model, using=self._db)
    
class LocationTypeChoice(models.TextChoices):
    Online = "Online", "Online"
    Physical = "Physical", "Physical"
    Abroad = "Abroad", "Abroad"
    

class JobLevel(models.TextChoices):
    A = "A", "Advanced"
    B = "B", "Beginner"
    I = "I","Intermediate"

# Create your models here.
class Job(models.Model):
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from="title", slugify_function=my_slugify_function)
    location = models.CharField(max_length=255, help_text="online, Nairobi, Qatar, etc")
    location_type = models.CharField(max_length=20, help_text="Online, Physical, Abroad, etc", choices=LocationTypeChoice.choices, default=LocationTypeChoice.Online)
    description = models.CharField(max_length=200)
    content = models.TextField()
    salary_offer = models.DecimalField(max_digits=12, decimal_places=2, default=10.89)
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        Profile, verbose_name=_("Job Author"), on_delete=models.SET_NULL, null=True, blank=True
    )
    level = models.CharField(choices=JobLevel, default=JobLevel.B, max_length=1)
    is_active = models.BooleanField(default=True)

    objects = JobManager()


    @property
    def is_popular(self):
        if self.job_applications >= 1000:
            return True
        return False
    
    @property
    def job_applications(self):
        return self.applications.count()
    
    @property
    def is_new(self):
        if self.date_posted <= timezone.now() - timezone.timedelta(days=30):
            return True
        return False
    

    def __str__(self):
        return self.title
    

def upload_application_resume(instance, filename):
    return f"applications/aplicant-{instance.applicant.pk}/{instance.job.pk}/{instance.pk}/{timezone.now().year}/{timezone.now().month}/{timezone.now().day}/{filename}"
    
class ApplicationStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    ACCEPTED = "ACCEPTED", "Accepted"
    REJECTED = "REJECTED", "Rejected"


class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile_job_applications")
    motivational_letter = models.TextField(blank=True, null=True)
    email_or_phone = models.CharField(max_length=100, blank=True, null=True)
    resume = models.FileField(upload_to=upload_application_resume, blank=True, null=True)
    status = models.CharField(choices=ApplicationStatus.choices, max_length=10, default=ApplicationStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Application for Job Id: {self.job.pk}"