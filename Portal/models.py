from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255,default='none',blank=True)
    last_name = models.CharField(max_length=255,default='none',blank=True)
    skills = models.TextField(blank=True,default='example: Python, Java, C++')
    cover_letter = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True, default='none')
    email= models.EmailField(default='none',blank=True)
    password = models.CharField(max_length=255, default='none',blank=True)
    location = models.CharField(max_length=100, blank=True)

class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=20,default='none')
    category = models.CharField(max_length=100,default='none')
    salary = models.CharField(max_length=100,default='none')
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()


class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email= models.EmailField()
    password = models.CharField(max_length=255)
    location = models.CharField(max_length=100,default='none',blank=True)
    hrname = models.CharField(max_length=255,default='none',blank=True)
    phone_number = models.CharField(max_length=20, default='none',blank=True)
    website = models.URLField(default='none',blank=True)
    about= models.TextField(default='none',blank=True)

class JobPosting(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    job = models.OneToOneField(Job, on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

class Application(models.Model):
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE,related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming you're using Django's built-in User model
    status = models.CharField(max_length=1, choices=[('P', 'Pending'), ('A', 'Accepted'), ('R', 'Rejected')], default='P')
    applied_at = models.DateTimeField(auto_now_add=True)
class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)