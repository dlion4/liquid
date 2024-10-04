from django.db import models
from django.urls import reverse

# Create your models here.


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.name

class CompanyTermsAndPolicy(models.Model):
    file = models.FileField(upload_to='policy')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.file.name}"
    

    def get_document_view_url(self):
        return reverse('view_policy', kwargs={'pk': self.pk})
    
    def save(self, *args, **kwargs):
        # Check if there's already an instance in the database
        existing_instance = CompanyTermsAndPolicy._default_manager.first()
        if existing_instance:
            # If an existing instance is found, use its ID for the new instance
            self.id = existing_instance.id
            existing_instance.delete()
        # Save the new instance
        super().save(*args, **kwargs)
    