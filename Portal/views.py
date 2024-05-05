from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login,logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Company,Profile,Job,JobPosting,Application,Message

def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username1')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser:
                return redirect('/admin/') 
            elif Company.objects.filter(email=username).exists():
                auth_login(request,user)
                company = Company.objects.get(email=username)
                # job_postings = JobPosting.objects.filter(company=company)
                request.session['company'] = company.id
                return redirect('hrdash')
            else:
                auth_login(request,user)
                candidate = Profile.objects.get(email=username)
                request.session['candidate'] = candidate.id
                return redirect('dash')
        else:
            
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})
    else:
        return render(request, 'login.html')

@login_required
def hrdash(request):
    company = request.session.get('company')
    company = Company.objects.get(id=company)
    job_postings = JobPosting.objects.filter(company=company)
    return render(request, 'hrdash.html', {'company': company, 'job_postings': job_postings})


def register(request):
    if request.method == 'POST':
        if 'company_name' in request.POST:  # Employer signup form submitted
            company_name = request.POST['company_name']
            email = request.POST['email']
            request.session['email'] = email
            password = request.POST['password']
            user = User.objects.create_user(username=company_name, email=email, password=password)
            user.save()
            company=Company.objects.create(user=user, name=company_name, email=email, password=password)
            company.save()
            return redirect('verify_otp')  # Redirect to login page after signup

        elif 'firstname' in request.POST:  # Candidate signup form submitted
            first_name = request.POST['firstname']
            last_name = request.POST['lastname']
            phone_number = request.POST['phonenumber']
            email = request.POST['email']
            request.session['email'] = email
            password = request.POST['password']
            user = User.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_name=last_name)
            user.save()
            candidate = Profile.objects.create(user=user,first_name=first_name,last_name=last_name,email=email ,phone_number=phone_number,password=password)
            candidate.save()
            return redirect('verify_otp') 

    return render(request, 'signup.html')  # Render the signup page

    
from django.core.mail import send_mail
from django.shortcuts import render, redirect

def verify_otp(request):
    email = request.session.get('email')
    otp = generate_otp()  # You need to implement a function to generate OTP
    send_otp_email(email, otp)
    if request.method == 'POST':
        otp1 = request.POST.get('otp')
        
        if otp == otp1 :  # Hardcoded OTP for demonstration
            return redirect('login')
        else:
            return render(request, 'verify_otp.html', {'email': email, 'error_message': 'Invalid OTP!'})

    # Generate OTP and send email


    return render(request, 'verify_otp.html', {'email': email})

def generate_otp():
    return '4726'  

def send_otp_email(email, otp):
    subject = 'OTP Verification'
    message = f'Your OTP for CareerForge signup is: {otp}'
    from_email = 'your-email@gmail.com'  # Replace with your Gmail address
    recipient_list = [email]

    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        print("OTP email sent successfully!")
    except Exception as e:
        print("Failed to send OTP email:", e)


@login_required
def profile(request):
    id=request.session.get('company')
    company=Company.objects.get(id=id)
    return render(request, 'profile.html', {'company': company})


@login_required
def upload_job(request):
    company_id = request.session.get('company')
    company = Company.objects.get(id=company_id)
    if request.method == 'POST':
        job_title = request.POST['jobTitle']
        job_description = request.POST['jobDescription']
        job_salary = request.POST['jobSalary']  
        job_location = request.POST['jobLocation']
        job_type = request.POST['jobType']
        job_category = request.POST['jobCategory']
        job_created_at = request.POST['jobCreated_at']
        job_deadline = request.POST['jobDeadline']

        job = Job.objects.create(
            title=job_title,
            description=job_description,
            salary=job_salary,
            location=job_location,
            type=job_type,
            category=job_category,
            created_at=job_created_at,
            deadline=job_deadline,
        )
        job.save()
        company = Company.objects.get(id=company_id)

        # Create job posting
        job_posting = JobPosting.objects.create(
            company=company,
            job=job,
        )
        job_posting.save()
        return render(request, 'upload_job.html', {'success_message': 'Job uploaded successfully!', 'company': company})

    else:
        return render(request, 'upload_job.html', { 'company': company})


@login_required
def application(request):
    id = request.session.get('company')
    company = Company.objects.get(id=id)
    applications = Application.objects.filter(status='P')  
    accept_applications = Application.objects.filter(status='accepted')
    return render(request, 'application.html', {'applications': applications, 'company': company,'accept_applications':accept_applications})
from django.shortcuts import get_object_or_404, redirect

def accept_application(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    application.status = 'accepted'
    application.save()
    return redirect('hrdash')

def reject_application(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    application.status = 'rejected'
    application.save()
    return redirect('hrdash')
def logout_view(request):
    logout(request)
    return redirect('login')
@login_required
def dash(request):
    if request.method == 'POST':
        job_title = request.POST.get('title')
        job_location = request.POST.get('location')
        job_postings = JobPosting.objects.all()
        job_postings=job_postings.filter(job__title__icontains=job_title)
        job_postings=job_postings.filter(job__location__icontains=job_location)
        type=request.POST.get('type')
        job_postings = job_postings.filter(job__type=type)
        job_postings = job_postings.filter(active=True)
        return render(request, 'dash.html', {'job_postings': job_postings})

    else:
        id=request.session.get('candidate')
        user=Profile.objects.get(id=id)
        user=user.user
        job_postings = JobPosting.objects.exclude(applications__applicant=user)
        print(job_postings)
        return render(request, 'dash.html', {'job_postings': job_postings})



@login_required
def apply_job(request, job_id):
    job_posting = get_object_or_404(JobPosting, id=job_id)

    Application.objects.create(job=job_posting, applicant=request.user)
    return redirect('dash')
@login_required
def edit_profile(request):
    id=request.session.get('company')
    company=Company.objects.get(id=id)
    if request.method=='POST':
        company.name=request.POST['name']
        company.email=request.POST['email']
        company.hrname=request.POST['hrname']
        company.website=request.POST['website']
        company.about=request.POST['about']
        company.phone_number=request.POST['phone_number']
        company.location=request.POST['location']
        company.save()
        return redirect('profile')
    return render(request, 'edit_profile.html',{'company':company})

@login_required
def resume(request):
    candidate=request.session.get('candidate')
    candidate=Profile.objects.get(id=candidate)
    return render(request, 'resume.html', {'candidate': candidate})

@login_required
def edit_resume(request):
    candidate=request.session.get('candidate')
    candidate=Profile.objects.get(id=candidate)
    if request.method=='POST':
        candidate.first_name=request.POST['first_name']
        candidate.last_name=request.POST['last_name']
        candidate.email=request.POST['email']
        candidate.phone_number=request.POST['phone_number']
        candidate.skills=request.POST['skills']
        candidate.cover_letter=request.POST['cover_letter']
        candidate.location=request.POST['location']
        candidate.save()
        return redirect('resume')
    return render(request, 'edit_resume.html', {'candidate': candidate})

@login_required
def my_jobs(request):
    applications = Application.objects.filter(applicant=request.user, status='accepted')
    return render(request, 'myjobs.html', {'applications': applications})

@login_required
def applied_jobs(request):
    candidate=request.session.get('candidate')
    candidate=Profile.objects.get(id=candidate)
    applications = Application.objects.filter(applicant=request.user)
    return render(request, 'applied_jobs.html', {'applications': applications, 'candidate': candidate})


def delete_job_posting(request, job_posting_id):
    job_posting = get_object_or_404(JobPosting, id=job_posting_id)
    job_posting.delete()
    return redirect('hrdash')

def viewdetails(request):
    job_posting_id=request.GET.get('job_posting_id')
    job_posting=JobPosting.objects.get(id=job_posting_id)
    return render(request, 'viewDetail.html', {'job_posting': job_posting})
from django.db.models import Q

@login_required
def messages(request):
    # Fetch all messages ordered by timestamp
    messages = Message.objects.all().order_by('-timestamp')

    # Initialize a dictionary to store messages indexed by sender and recipient
    unique_messages = {}

    # Loop through each message
    for message in messages:
        if message.sender.username == request.user.username:
            key = (message.recipient.username)
            if key not in unique_messages:
                unique_messages[key] = {
                'sender': message.sender.username,
                'sender_id': message.sender.id,  # Add sender's ID
                'recipient': message.recipient.username,
                'recipient_id': message.recipient.id,
                'content': message.content,
                'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }
    unique_messages_list = list(unique_messages.values())
    messages=unique_messages_list
    user=request.user
    if Company.objects.filter(user=user).exists():
        user=True
    else:
        user=False
    return render(request, 'messages.html', {'messages': messages,'user':user})
from django.core.serializers import serialize

@login_required
def room(request):
    recipient_id = request.GET.get('id')
    request.session['recipient_id'] = recipient_id
    print(recipient_id)
    messages = Message.objects.filter(recipient_id=recipient_id)
    serialized_messages = list(messages)
    senders = [message.sender.username for message in messages]
    recipient=User.objects.get(id=recipient_id)
    serialized_messages = serialize('json', messages)
    print(senders)
    return render(request,'room.html',{'messages': serialized_messages,'senders':senders,'recipient':recipient})

def get_messages(request):
    recipient_id = request.session.get('recipient_id')  # Fix the parameter name
    print(recipient_id)
    messages = Message.objects.filter(recipient_id=recipient_id)
    serialized_messages = [
        {
            'sender': message.sender.username,
            'content': message.content,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
        for message in messages
    ]
    return JsonResponse({'messages': serialized_messages})

@login_required
def send_message(request):
    if request.method == 'POST':
        content = request.POST.get('content', '')
        recipient_id = request.session.get('recipient_id')
        sender = request.user
        print(sender)  
        csrf_token = request.POST.get('csrfmiddlewaretoken')
        # Now create and save the message
        # Make sure to handle validation, error handling, etc.
        messages = Message.objects.create(sender=sender, recipient_id=recipient_id, content=content)
        return JsonResponse({'success': True},{'messages': messages})

    # Handle other HTTP methods or invalid requests
    return JsonResponse({'error': 'Invalid request'}, status=400)