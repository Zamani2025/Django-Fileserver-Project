from django.db import models
from core.models import CustomUser
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify

# File Model
class FileModel(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    slug = models.SlugField()
    description = models.TextField()
    upload_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='admin')
    file = models.FileField(upload_to='files/', null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['png', 'pdf', 'jpg', 'jpeg', 'docx'])])
    download_count = models.PositiveIntegerField(default=0)
    email_count = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created']

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.title)

        return super().save(*args, **kwargs)
    
    # Download File Counter Method
    def download(self):
        self.download_count += 1
        self.save()

    # Send Email Counter Method
    def sendEmail(self):
        self.email_count += 1
        self.save()

