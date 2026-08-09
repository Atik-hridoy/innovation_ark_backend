from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    tags = models.JSONField(default=list, null=True, blank=True)
    metric_value = models.CharField(max_length=100, null=True, blank=True)
    metric_label = models.CharField(max_length=100, null=True, blank=True)
    mockup_1 = models.ImageField(upload_to='projects/', null=True, blank=True)
    mockup_2 = models.ImageField(upload_to='projects/', null=True, blank=True)
    mockup_3 = models.ImageField(upload_to='projects/', null=True, blank=True)
    mockup_4 = models.ImageField(upload_to='projects/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title or f"Project {self.id}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"

class FAQ(models.Model):
    question = models.CharField(max_length=500)
    answer = models.TextField()
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.question

class SiteSettings(models.Model):
    facebook_url = models.URLField(max_length=500, null=True, blank=True, default="https://facebook.com")
    whatsapp_number = models.CharField(max_length=50, null=True, blank=True, default="1234567890")
    phone_number = models.CharField(max_length=50, null=True, blank=True, default="+1234567890")
    email_address = models.EmailField(null=True, blank=True, default="contact@innovativeark.com")
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SiteSettings, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Site Settings"
