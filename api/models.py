from django.db import models
from django.contrib.auth.models import User

class Resume(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('processed', 'Processed'),
        ('not_processed', 'Not Processed'),
    ]

    candidate_name = models.CharField(max_length=240,blank=True,null=True)
    personal_information = models.TextField(blank=True,null=True)
    education_history = models.TextField(blank=True,null=True)
    work_experience = models.TextField(blank=True,null=True)
    skills = models.TextField(blank=True,null=True)
    projects = models.TextField(blank=True,null=True)
    certifications = models.TextField(blank=True,null=True)
    minified_context = models.TextField(blank=True,null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')

    file_path = models.CharField(max_length=240, blank=True, null=True)

    def __str__(self):
        return f"Resume {self.id} - {self.created_by.username}"
    

class ChatHistory(models.Model):
    user = models.CharField(max_length=240)
    prompt = models.TextField()
    response = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ChatHistory {self.id} - {self.user}"