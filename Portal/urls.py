from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [

    path('',views.index,name='index'),
    path('login',views.login,name='login'),
    path('register',views.register,name='register'),
    path('hrdash',views.hrdash,name='hrdash'),
    path('profile',views.profile,name='profile'),
    path('upload_job',views.upload_job,name='upload_job'),
    path('application',views.application,name='application'),
    path('logout',views.logout_view,name='logout'),
    path('dash',views.dash,name='dash'),
    path('apply_job/<int:job_id>/', views.apply_job, name='apply_job'),
    path('accept_application/<int:application_id>/', views.accept_application, name='accept_application'),
    path('reject_application/<int:application_id>/', views.reject_application, name='reject_application'),
    path('edit_profile',views.edit_profile,name='edit_profile'),
    path('resume',views.resume,name='resume'),
    path('edit_resume',views.edit_resume,name='edit_resume'),
    path('applied_jobs',views.applied_jobs,name='applied_jobs'),
    path('myjobs',views.my_jobs,name='myjobs'),
    path('delete_job_posting/<int:job_posting_id>/', views.delete_job_posting, name='delete_job_posting'),
    path('viewdetails', views.viewdetails, name='viewdetails'),    
    path('messages', views.messages, name='messages'),
    path('room', views.room, name='room'),
    path('get_messages/', views.get_messages, name='get_messages'),
    path('send_message/', views.send_message, name='send_message'),
    path('verify_otp', views.verify_otp, name='verify_otp'),

] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)