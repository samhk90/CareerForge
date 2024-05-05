from django.contrib import admin
from .models import JobPosting, Application, Profile, Job,Company,Message

# Register your models here.
admin.site.register(JobPosting)
admin.site.register(Application)
admin.site.register(Profile)
admin.site.register(Job)
admin.site.register(Company)
admin.site.register(Message)
admin.site.site_title = 'CareerForge Admin'
admin.site.site_header = 'CareerForge Admin'