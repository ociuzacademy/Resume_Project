from django.shortcuts import render,redirect,get_object_or_404
from.models import *
from django.http import HttpResponse,HttpResponseRedirect
# from .forms import DocumentForm
# from resumeapp.models import job
from django.contrib import messages
from .models import tbl_register

from .resume_detect import *
import ast
from django.conf import settings




# Create your views here.
def index(request):
    return render(request,'index.html')

def user_register(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        pswd = request.POST.get('pswd')
        adrs = request.POST.get('adrs')
        phn = request.POST.get('phn')
        plc = request.POST.get('plc')

        gender = request.POST.get('gender')
        dob = request.POST.get('dob')

        qualification = request.POST.get('qualification')

        tbl_register.objects.create(
            name=name,
            uname=uname,
            email=email,
            pswd=pswd,
            adrs=adrs,
            phn=phn,
            plc=plc,
            dob=dob if dob else None,
            gender=gender,
            qualification=qualification,
            utype='user'
        )

        return render(request, 'index.html')

    return render(request, 'user_register.html')


def login(request):

    if request.method == "POST":

        pswd = request.POST['pswd']
        email = request.POST['email']


        # USER
        var = tbl_register.objects.filter(
            pswd=pswd,
            email=email,
            utype='user'
        )


        # RECRUITER
        var2 = tbl_register.objects.filter(
            pswd=pswd,
            email=email,
            utype='recruiter'
        )


        # ADMIN
        var4 = tbl_register.objects.filter(
            pswd=pswd,
            email=email,
            utype='admin'
        )


        if var.exists():

            x = var.first()

            request.session['id'] = x.id
            request.session['username'] = x.uname
            request.session['name'] = x.name

            return redirect('user_home')


        elif var2.exists():

            x = var2.first()

            request.session['id'] = x.id
            request.session['name'] = x.name

            return redirect('recruiter_home')


        elif var4.exists():

            x = var4.first()

            request.session['id'] = x.id
            request.session['name'] = x.name

            return redirect('admin_home')


        else:

            txt = """
            <script>
                alert("Invalid user Credentials....");
                window.location='/';
            </script>
            """

            return HttpResponse(txt)


    else:

        return render(request, "login.html")

    
def logout(request):
    
    request.session.clear()
    txt = """<script>alert("Logout Sucessful....");window.location='/';</script>"""
    return render(request,"index.html")




# <----------------------------------USER----------------------------------------->

from django.shortcuts import render, redirect

from .models import (
    tbl_register,
    tbl_jobdetails,
    tbl_userresume,
    tbl_userresume2,
    tb_skill,
    tbl_user_apply_job,
    tbl_notification,
)


def user_home(request):

    # -----------------------------------------
    # GET LOGGED-IN USER ID
    # -----------------------------------------

    user_id = request.session.get('id')

    if not user_id:
        return redirect('login')


    # -----------------------------------------
    # GET USER
    # -----------------------------------------

    user = tbl_register.objects.filter(
        id=user_id,
        utype='user'
    ).first()


    if not user:
        request.session.flush()
        return redirect('login')


    # -----------------------------------------
    # DASHBOARD COUNTS
    # -----------------------------------------

    # Total available jobs
    job_count = tbl_jobdetails.objects.count()


    # User's uploaded resumes
    resume_count = tbl_userresume.objects.filter(
        user=user
    ).count()


    # User's second resume table
    resume2_count = tbl_userresume2.objects.filter(
        user=user
    ).count()


    # User's skills
    skill_count = tb_skill.objects.filter(
        user_id=user
    ).count()


    # Jobs applied by the user
    applied_job_count = tbl_user_apply_job.objects.filter(
        user=user
    ).count()


    # Notifications related to user's applications
    notification_count = tbl_notification.objects.filter(
        application__user=user
    ).count()


    # -----------------------------------------
    # PROFILE COMPLETION
    # -----------------------------------------

    total_fields = 7
    completed_fields = 0


    if user.name:
        completed_fields += 1


    if user.email:
        completed_fields += 1


    if user.phn:
        completed_fields += 1


    if user.adrs:
        completed_fields += 1


    if user.gender:
        completed_fields += 1


    if user.qualification:
        completed_fields += 1


    if user.profile_pic:
        completed_fields += 1


    profile_completion = int(
        (completed_fields / total_fields) * 100
    )


    # -----------------------------------------
    # CONTEXT
    # -----------------------------------------

    context = {

        'user': user,

        'job_count': job_count,

        'resume_count': resume_count,

        'resume2_count': resume2_count,

        'skill_count': skill_count,

        'applied_job_count': applied_job_count,

        'notification_count': notification_count,

        'profile_completion': profile_completion,

    }


    # -----------------------------------------
    # RENDER
    # -----------------------------------------

    return render(
        request,
        'user/user_home.html',
        context
    )


# views.py

from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import tbl_register


def user_viewprofile(request):

    id = request.session['id']

    user_profile = tbl_register.objects.get(id=id)

    return render(
        request,
        'user/user_viewprofile.html',
        {'user_profile': user_profile}
    )



def user_editprofile(request):

    id = request.session['id']

    user = tbl_register.objects.get(id=id)

    if request.method == 'POST':

        user.name = request.POST.get('name')
        user.bio = request.POST.get('bio')
        user.adrs = request.POST.get('adrs')
        user.phn = request.POST.get('phn')
        user.gender = request.POST.get('gender')
        user.plc = request.POST.get('plc')

        # profile image upload
        if request.FILES.get('profile_pic'):
            user.profile_pic = request.FILES.get('profile_pic')

        user.save()

        return HttpResponseRedirect('/user_viewprofile/')

    return render(
        request,
        'user/user_editprofile.html',
        {'user_profile': user}
    )


# def user_uploadresume(request):
#     id=request.session['id']
#     if request.method=='POST':
#         user_id=request.session['id']
#         experience = request.POST.get('experience')
#         resume = request.FILES.get('resume')
#         # Fetch the user instance using the user_id
#         user_instance = tbl_register.objects.get(id=user_id)
#         user_resume = tbl_userresume.objects.create(user=user_instance,experience=experience,resume=resume).save()
#         return HttpResponseRedirect('/user_uploadresume/')
#     else:
#         user_profile=tbl_register.objects.all().filter(id=id)
#         return render(request,'user/user_uploadresume.html',{'user_profile':user_profile})


# def user_uploadresume(request):
#     if request.method == "POST":
#         user_id = request.session.get('id')
#         resume = request.FILES.get('resume')
#         if user_id and resume:
#             user_instance = tbl_register.objects.get(id=user_id)
#             existing_resume = tbl_userresume.objects.filter(user_id=user_id).first()
            
            
            
#             if existing_resume:
#                 existing_resume.resume.delete()
#                 existing_resume.delete()

#             # Upload new resume to tbl_userresume
#             data = tbl_userresume(user_id=user_instance, resume=resume)
#             data.save()

#             # Upload the same resume to tbl_userresume2
#             content = resume.read()
#             file_name = default_storage.save(f'resumes/{resume.resume}', ContentFile(content))
                
                
#                     existing_resume.resume = resume
#                     existing_resume.save()
#                     image_url = existing_resume.resume.url
#                     result = resumes(image_url)
#                     latest_skill_instance = tb_skill.objects.latest('id')
#                     latest_skill_instance.user_id = user_instance
#                     latest_skill_instance.save()
#                     return render(request, 'user/user_home.html', {'message': 'success'})
                
            
#             else:
#                 data = tbl_userresume(user_id=user_id, resume=resume)
#                 data.save()
#                 image_url = data.resume.url
#                 result = resumes(image_url)

#                 latest_skill_instance = tb_skill.objects.latest('id')
#                 latest_skill_instance.user_id = user_instance
#                 latest_skill_instance.save()
#                 return render(request, 'user/user_home.html', {'message': 'success'})
#         else:
#             return render(request, 'user/user_home.html', {'message': 'error'})
#     else:
#       id=request.session['id']
#       user_profile=tbl_register.objects.all().filter(id=id)
#       return render(request,'user/user_uploadresume.html',{'user_profile':user_profile})

import os

def user_uploadresume(request):

    if request.method == "POST":

        user_id = request.session.get('id')

        resume = request.FILES.get('resume')

        experience = request.POST.get('experience')

        if user_id and resume:

            user_instance = tbl_register.objects.get(id=user_id)

            # Delete only this user's previous resumes
            existing_resumes = tbl_userresume.objects.filter(
                user_id=user_id
            )

            for existing_resume in existing_resumes:

                old_resume_path = existing_resume.resume.path

                try:

                    if os.path.exists(old_resume_path):
                        os.remove(old_resume_path)

                except Exception as e:

                    print("DELETE ERROR =", e)

                existing_resume.delete()

            # Save resume
            data_userresume = tbl_userresume.objects.create(
                user_id=user_id,
                resume=resume,
                experience=experience
            )

            # Save backup resume
            tbl_userresume2.objects.create(
                user=user_instance,
                resume1=resume,
                experience=experience
            )

            # Extract and save skills
            resumes(data_userresume.resume, user_instance)

            return redirect('user_view_jobs')

        else:

            return render(
                request,
                'user/user_home.html',
                {'message': 'error'}
            )

    else:

        id = request.session['id']

        user_profile = tbl_register.objects.filter(id=id)

        return render(
            request,
            'user/user_uploadresume.html',
            {'user_profile': user_profile}
        )

def user_view_resume(request):
    user_id = request.session.get('id')
    data = tbl_userresume2.objects.filter(
        user_id=user_id
    ).order_by('-id').first()

    return render(
        request,
        'user/download.html',
        {'data': data, 'request': request}  # add request here
    )

def user_jobviewmore(request, job_id):
    job = tbl_jobdetails.objects.get(id=job_id)
    company_name = tbl_register.objects.get(id=job.company_id).name
    context = {
        'company_name':company_name,
        'job': job}
    return render(request, 'user/user_jobviewmore.html', context)

    



        
from .models import tbl_register, tbl_userresume


# def user_uploadresume(request):
#     id = request.session['id']

#     if request.method == 'POST':
#         user_id = request.session['id']
#         experience = request.POST.get('experience')
#         resume = request.FILES.get('resume')

#         # Fetch the user instance using the user_id
#         user_instance = tbl_register.objects.get(id=user_id)
#         # Get all user resume instances
#         user_resumes = tbl_userresume.objects.filter(user=user_instance)
#         # Check the number of instances
#         if user_resumes.exists():
#             # If there is at least one instance, update the first one
#             user_resume = user_resumes.first()
#             user_resume.experience = experience
#             user_resume.resume = resume
#             user_resume.save()
#         else:
#             # If no instance exists, create a new one
#             user_resume = tbl_userresume.objects.create(user=user_instance, experience=experience, resume=resume)

#         return HttpResponseRedirect('/user_uploadresume/')
#     else:
#         user_profile = tbl_register.objects.filter(id=id)
#         return render(request, 'user/user_uploadresume.html', {'user_profile': user_profile})



import ast
import json

def user_view_jobs(request):

    user_id = request.session.get('id')

    try:

        last_skill = tb_skill.objects.filter(
            user_id=user_id
        ).values_list('skill', flat=True).last()

        print("LAST SKILL =", last_skill)

        if not last_skill:

            return render(
                request,
                'user/user_view_jobs.html',
                {'joblist': []}
            )

        # Convert JSON string back to list
        skill_list = json.loads(last_skill)

        print("SKILL LIST =", skill_list)

        matching_jobs = tbl_jobdetails.objects.none()

        for skill in skill_list:

            jobs = tbl_jobdetails.objects.filter(
                jobskills__icontains=skill
            )

            print("MATCHING JOBS FOR", skill, "=", jobs)

            matching_jobs = matching_jobs | jobs

        # Remove duplicates
        matching_jobs = matching_jobs.distinct()

        print("FINAL JOBS =", matching_jobs)

        return render(
            request,
            'user/user_view_jobs.html',
            {'joblist': matching_jobs}
        )

    except Exception as e:

        print("ERROR =", e)

        return render(
            request,
            'user/user_view_jobs.html',
            {'error_message': str(e)}
        )

from django.shortcuts import render
# from .models import tbl_user_apply_job

def user_view_applied_jobs(request):
    user_id = request.session.get('id')

    try:
        # Get the jobs that the user has applied for
        applied_jobs = tbl_user_apply_job.objects.filter(user_id=user_id)

        return render(request, 'user/user_view_applied_jobs.html', {"applied_jobs": applied_jobs})

    except Exception as e:
        return render(request, 'user/user_view_applied_jobs.html', {"error_message": str(e)})




    



from .models import tbl_register, tbl_userresume



def user_apply_job(request, job_id):
    job = get_object_or_404(tbl_jobdetails, pk=job_id)
    user_id = request.session.get('id')

    if user_id is not None:
        user = get_object_or_404(tbl_register, pk=user_id)
        resume_entry = tbl_userresume2.objects.filter(user_id=user_id).order_by('-id').first()

        if resume_entry:
            experience = resume_entry.experience
            resume = resume_entry  # Assign the entire tbl_userresume2 instance
        else:
            experience = "0"
            resume = None

        application = tbl_user_apply_job.objects.create(
            user=user,
            job=job,
            status="applied",
            resume=resume
        )
        return redirect('user_home')

    return render(request, 'user/user_view_jobs.html')



# def user_apply_job(request, job_id):
#     if request.method == 'POST':
#         experience = request.POST.get('experience')
#         resume = request.FILES.get('resume')
        

#         user_id = request.session['id']
#         user_instance = tbl_register.objects.get(id=user_id)

#         user_resumes = tbl_userresume.objects.filter(user=user_instance)

#         if user_resumes.exists():
#             user_resume = user_resumes.first()
#             user_resume.experience = experience
#             user_resume.resume = resume
#             user_resume.save()
#         else:
#             tbl_userresume.objects.create(user=user_instance, experience=experience, resume=resume)

#         return HttpResponseRedirect('/user_uploadresume/')
#     else:
#         user_profile = tbl_register.objects.filter(id=request.session['id'])
#         return render(request, 'user/user_apply_jobs.html', {'user_profile': user_profile, 'job_id': job_id})







from django.shortcuts import render
from .models import tbl_register


def recruiter_register(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        pswd = request.POST.get('pswd')
        adrs = request.POST.get('adrs')
        phn = request.POST.get('phn')
        plc = request.POST.get('plc')

        # Get company logo
        profile_pic = request.FILES.get('logo')

        tbl_register.objects.create(
            name=name,
            uname=uname,
            email=email,
            pswd=pswd,
            adrs=adrs,
            phn=phn,
            plc=plc,
            profile_pic=profile_pic,
            utype='recruiter',
            status='pending'
        )

        return render(request, 'index.html')

    return render(request, 'recruiter_register.html')


from django.shortcuts import render, redirect

from .models import (
    tbl_register,
    tbl_jobdetails,
    tbl_user_apply_job,
)


def recruiter_home(request):

    # -----------------------------------------
    # GET LOGGED-IN RECRUITER
    # -----------------------------------------

    recruiter_id = request.session.get('id')

    if not recruiter_id:
        return redirect('login')


    recruiter = tbl_register.objects.filter(
        id=recruiter_id,
        utype='recruiter'
    ).first()


    if not recruiter:
        request.session.flush()
        return redirect('login')


    # -----------------------------------------
    # RECRUITER JOBS
    # -----------------------------------------

    jobs = tbl_jobdetails.objects.filter(
        company=recruiter
    ).order_by('-id')


    # Total jobs posted by recruiter
    job_count = jobs.count()


    # -----------------------------------------
    # APPLICATIONS
    # -----------------------------------------

    applications = tbl_user_apply_job.objects.filter(
        job__company=recruiter
    )


    # Total applications
    application_count = applications.count()


    # Pending applications
    pending_count = applications.filter(
        status='applied'
    ).count()


    # Shortlisted applications
    shortlisted_count = applications.filter(
        status='shortlisted'
    ).count()


    # Rejected applications
    rejected_count = applications.filter(
        status='rejected'
    ).count()


    # -----------------------------------------
    # RECENT JOBS
    # -----------------------------------------

    recent_jobs = jobs[:5]


    # -----------------------------------------
    # RECENT APPLICATIONS
    # -----------------------------------------

    recent_applications = applications.select_related(
        'user',
        'job'
    ).order_by('-id')[:5]


    # -----------------------------------------
    # CONTEXT
    # -----------------------------------------

    context = {

        'recruiter': recruiter,

        'job_count': job_count,

        'application_count': application_count,

        'pending_count': pending_count,

        'shortlisted_count': shortlisted_count,

        'rejected_count': rejected_count,

        'recent_jobs': recent_jobs,

        'recent_applications': recent_applications,

    }


    return render(
        request,
        'recruiter/recruiter_home.html',
        context
    )


def recruiter_viewprofile(request):
    # Assuming you have a way to identify the user, replace '<user_id>' with the actual user ID or use the user from the request if using authentication
    id=request.session['id']
    user_profile = tbl_register.objects.get(id=id)  

    context = {'user_profile': user_profile}
    return render(request, 'recruiter/recruiter_viewprofile.html', context)

def recruiter_editprofile(request):
    id=request.session['id']
    if request.method=='POST':
        name=request.POST.get('name')
        bio=request.POST.get('bio')
        adrs=request.POST.get('adrs')
        phn=request.POST.get('phn')
        plc=request.POST.get('plc')
        tbl_register.objects.all().filter(id=id).update(name=name,bio=bio,adrs=adrs,phn=phn,plc=plc)
        return HttpResponseRedirect('/recruiter_viewprofile/')
    else:
        user_profile=tbl_register.objects.all().filter(id=id)
        return render(request,'recruiter/recruiter_editprofile.html',{'user_profile':user_profile})


def recruiter_addjob(request):
    if request.method == 'POST':
        company_id = request.session.get('id')
        jobtitle = request.POST.get('jobtitle')
        jobtype = request.POST.get('jobtype')
        jobvacancy = request.POST.get('jobvacancy')
        jobdate1 = request.POST.get('jobdate1')
        jobdate2 = request.POST.get('jobdate2')
        jobexp1 = request.POST.get('jobexp1')
        jobexp2 = request.POST.get('jobexp2')
        joblocation = request.POST.get('joblocation')
        jobskills = request.POST.get('jobskills')
        jobdescription = request.POST.get('jobdescription')

        try:
            # Fetch the company instance using the company_id
            company_instance = tbl_register.objects.get(id=company_id)

            # Create a new job instance and associate it with the company
            new_job = tbl_jobdetails.objects.create(
                company=company_instance,
                jobtitle=jobtitle,
                jobtype=jobtype,
                jobvacancy=jobvacancy,
                jobdate1=jobdate1,
                jobdate2=jobdate2,
                jobexp1=jobexp1,
                jobexp2=jobexp2,
                joblocation=joblocation,
                jobskills=jobskills,
                jobdescription=jobdescription
            )

            alert_message = "Job added successfully"
            return render(request, "recruiter/recruiter_addjob.html", {'alert_message': alert_message})  # Redirect to the same page after successful submission
        except tbl_register.DoesNotExist:
            messages.error(request, 'Company not found')
            return render(request, "recruiter/recruiter_addjob.html")  # Redirect to the same page with an error message
    else:
        return render(request, "recruiter/recruiter_addjob.html")
    

def recruiter_viewjob(request):
    company_id = request.session.get('id')

    # Correct the filter to use company_id
    recruiter_joblist = tbl_jobdetails.objects.filter(company_id=company_id)

    company_name = tbl_register.objects.get(id=company_id).name
    # profile_pic = tbl_register.objects.get(id=company_id).profile_pic

    context = {
        'recruiter_joblist': recruiter_joblist,
        'company_name': company_name,
    }
    print('context',context)

    return render(request, 'recruiter_viewjob.html', context)
    
def recruiter_view_pending_applicants(request):
    company_id = request.session.get('id')
    recruiter_joblist = tbl_jobdetails.objects.filter(company_id=company_id)

    pending_applicants = []

    for job in recruiter_joblist:
        job_id = job.id
        job_title = job.jobtitle
        job_applicants = tbl_user_apply_job.objects.filter(job_id=job_id, status='applied')
        pending_applicants.append({'job_title': job_title, 'applicants': job_applicants})

    context = {'pending_applicants': pending_applicants}
    return render(request, 'recruiter/recruiter_view_pending_applicants.html', context)
    

def recruiter_view_shortlisted_applicants(request):
    company_id = request.session.get('id')
    recruiter_joblist = tbl_jobdetails.objects.filter(company_id=company_id)

    pending_applicants = []

    for job in recruiter_joblist:
        job_id = job.id
        job_title = job.jobtitle
        job_applicants = tbl_user_apply_job.objects.filter(job_id=job_id, status='shortlisted')
        pending_applicants.append({'job_title': job_title, 'applicants': job_applicants})

    context = {'pending_applicants': pending_applicants}
    return render(request, 'recruiter/recruiter_view_shortlisted_applicants.html', context)

def recruiter_view_rejected_applicants(request):
    company_id = request.session.get('id')
    recruiter_joblist = tbl_jobdetails.objects.filter(company_id=company_id)

    pending_applicants = []

    for job in recruiter_joblist:
        job_id = job.id
        job_title = job.jobtitle
        job_applicants = tbl_user_apply_job.objects.filter(job_id=job_id, status='rejected')
        pending_applicants.append({'job_title': job_title, 'applicants': job_applicants})

    context = {'pending_applicants': pending_applicants}
    return render(request, 'recruiter/recruiter_view_rejected_applicants.html', context)

def recruiter_jobviewmore(request, job_id):
    job = tbl_jobdetails.objects.get(id=job_id)
    company_name = tbl_register.objects.get(id=job.company_id).name
    context = {
        'company_name':company_name,
        'job': job}
    return render(request, 'recruiter_jobviewmore.html', context)






def recruiter_updatejob(request, job_id):
    job = tbl_jobdetails.objects.get(id=job_id)

    if request.method == 'POST':
        jobtitle = request.POST.get('jobtitle')
        jobtype = request.POST.get('jobtype')
        jobvacancy = request.POST.get('jobvacancy')
        jobdate1 = request.POST.get('jobdate1')
        jobdate2 = request.POST.get('jobdate2')
        jobexp1 = request.POST.get('jobexp1')
        jobexp2 = request.POST.get('jobexp2')
        joblocation = request.POST.get('joblocation')
        jobskills = request.POST.get('jobskills')
        jobdescription = request.POST.get('jobdescription')

        # Update job details
        tbl_jobdetails.objects.filter(id=job_id).update(
            jobtitle=jobtitle, jobtype=jobtype, jobvacancy=jobvacancy,
            jobdate1=jobdate1,jobdate2=jobdate2, jobexp1=jobexp1, jobexp2=jobexp2,
            joblocation=joblocation, jobskills=jobskills,
            jobdescription=jobdescription
        )

        alert_message1 = "Job Updated successfully"
        return render(request, "recruiter/recruiter_updatejob.html",{'alert_message1':alert_message1,'job':job})

    else:
        # Fetch existing job details for rendering the form
        # data = tbl_jobdetails.objects.get(id=job_id)
        job.jobdate1 = job.jobdate1.strftime('%Y-%m-%d')
        job.jobdate2 = job.jobdate2.strftime('%Y-%m-%d')
        return render(request, "recruiter/recruiter_updatejob.html", {'data': job})
    

def recruiter_deletejob(request, job_id):
    job = tbl_jobdetails.objects.get(id=job_id)

    if request.method == 'POST':
        # Check if the user has confirmed the deletion
        if request.POST.get('confirm_delete'):
            job.delete()
            return redirect('/recruiter_viewjob/')

    return render(request, 'recruiter/recruiter_viewjob.html', {'job': job})



def resume_skill():
    entries = tbl_jobdetails.objects.values('id', 'jobskills')  
    jobskills = [entry['jobskills'] for entry in entries] 
    print("resume_skill......",jobskills) 
    ids = [entry['id'] for entry in entries] 
    return jobskills, ids


def shortlistCandidate(request, appli_id):
    recr_id = request.session.get('id')
    application = tbl_user_apply_job.objects.get(id=appli_id, job_id__company_id=recr_id)
    application.status = "shortlisted"
    application.save()
    message = f"Application for job {application.job} by {application.user} shortlisted successfully."
    return redirect('recruiter_view_pending_applicants')



def rejectCandidate(request, appli_id):
    recr_id = request.session.get('id')
    application = tbl_user_apply_job.objects.get(id=appli_id, job_id__company_id=recr_id)
    application.status = "rejected"
    application.save()
    message = f"Application for job {application.job} by {application.user} shortlisted successfully."
    return redirect('recruiter_view_pending_applicants')

# def recruiter_view_applicants(request, job_id):
    job = get_object_or_404(tbl_jobdetails, id=job_id)
    applicants = tbl_user_apply_job.objects.filter(job_id=job,status="shortlisted")
    context = {
        'job': job,
        'applicants': applicants,
    }

    return render(request, 'recruiter/recruiter_view_applicants.html', context)

def recruiter_view_applicants(request, job_id):
    # job = get_object_or_404(tbl_jobdetails, id=job_id)
    recruiter_joblist = tbl_jobdetails.objects.filter(id=job_id)
    pending_applicants = []
    for job in recruiter_joblist:
        job_id = job.id
        job_title = job.jobtitle
        job_applicants = tbl_user_apply_job.objects.filter(job_id=job_id, status='shortlisted')
        pending_applicants.append({'job_title': job_title, 'applicants': job_applicants})

    context = {'pending_applicants': pending_applicants}
    return render(request, 'recruiter/recruiter_view_applicants.html', context)



from django.utils import timezone
from .models import tbl_user_apply_job, tbl_notification

def recruiter_create_notification(request, appli_id):
    if request.method == 'POST':
        applicant = get_object_or_404(tbl_user_apply_job, id=appli_id)
        message = request.POST.get('message')
        notification = tbl_notification.objects.create(
            application=applicant,
            timezone=timezone.now(),  # Ensure there's no conflict with variable names
            message=message
        )
        applicant.notification_sent = True
        applicant.save()
        # Redirect to a success page or any other view
        return render(request, 'recruiter/recruiter_home.html')  # Change 'recruiter_create_notification.html' to the actual template name
    return render(request, 'recruiter/recruiter_create_notification.html')



def user_cancel_application(request, appli_id):
    if request.method == 'POST':
        user_application = get_object_or_404(tbl_user_apply_job, id=appli_id)
        user_application.delete()

        messages.success(request, 'Application canceled successfully.')
        return redirect('user_view_applied_jobs')

    return redirect('user_view_applied_jobs')
#----------------------Admin---------------------------------------

from django.shortcuts import render
from .models import tbl_register, tbl_jobdetails


def admin_home(request):

    user_count = tbl_register.objects.filter(
        utype='user'
    ).count()

    approved_count = tbl_register.objects.filter(
        utype='recruiter',
        status='approved'
    ).count()

    pending_count = tbl_register.objects.filter(
        utype='recruiter',
        status='pending'
    ).count()

    rejected_count = tbl_register.objects.filter(
        utype='recruiter',
        status='rejected'
    ).count()

    job_count = tbl_jobdetails.objects.count()

    return render(request, 'admin_home.html', {
        'user_count': user_count,
        'approved_count': approved_count,
        'pending_count': pending_count,
        'rejected_count': rejected_count,
        'job_count': job_count,
    })


def admin_viewpending(request):
    # Assuming you have a 'status' field in your tbl_jobdetails model
    pending_recruiters = tbl_register.objects.filter(status='pending')
    return render(request, 'admin/admin_viewpending.html', {'pending_recruiters': pending_recruiters})

def admin_viewapproved(request):
    # Assuming you have a 'status' field in your tbl_jobdetails model
    approved_recruiters = tbl_register.objects.filter(status='approved')
    return render(request, 'admin/admin_viewapproved.html', {'approved_recruiters': approved_recruiters})

def admin_viewrecruiters(request):
    # Assuming you have a 'status' field in your tbl_jobdetails model
    approved_recruiters = tbl_register.objects.filter(status='approved')
    return render(request, 'admin/admin_viewrecruiters.html', {'approved_recruiters': approved_recruiters})

def admin_viewrejected(request):
    # Assuming you have a 'status' field in your tbl_jobdetails model
    rejected_recruiters = tbl_register.objects.filter(status='rejected')
    return render(request, 'admin/admin_viewrejected.html', {'rejected_recruiters': rejected_recruiters})

def admin_approve(request, user_id):
    # Assuming YourModel has a 'status' field
    user = tbl_register.objects.get(id=user_id)

    if request.method == 'POST':
        # Update the status or perform other necessary actions
        user.status = 'approved'
        user.save()
        # Redirect to a success page or another view
        return redirect('/admin_viewpending/')

    return render(request, 'admin_viewpending.html', {'pending_recruiters': user})

def admin_reject(request, user_id):
    recruiter = tbl_register.objects.get(id=user_id)
    if request.method == 'POST':
        recruiter.status = 'rejected'
        recruiter.save()
        return redirect('/admin_viewpending/')

    return render(request, 'admin_viewpending.html', {'recruiter': recruiter})
from django.shortcuts import render, get_object_or_404

def admin_viewjob(request, company_id):
    company = get_object_or_404(tbl_register, id=company_id)

    joblist = tbl_jobdetails.objects.filter(company_id=company_id)

    return render(request, 'admin_viewjob.html', {
        'joblist': joblist,
        'company_name': company.name,
    })

def view_users(request):
    users = tbl_register.objects.filter(utype='user')
    return render(request, 'admin/admin_view_user.html', {'users': users})
    
    
    



# from .utils import send_registration_email

# def register_user(request):
#     # Your user registration logic here

#     # Assuming you have obtained the user's email during registration
#     user_email = 'user@example.com'  # Replace with the actual user's email
#     send_registration_email(user_email)


import os
import re
import spacy
from PyPDF2 import PdfReader
from docx import Document
from resumeapp.models import*
from resumeapp.views import* 
from django.http import HttpRequest
import requests

# Load the spaCy model 

nlp = spacy.load("en_core_web_sm")


# predefined_skills = ["ios", "c++", "Machine Learning", "Data Analysis", "Android"]

# predefined_skills,company = resume_skill()
# print("predefined_skills......",predefined_skills)
# predefined_skills = ["ios", "c++", "Machine Learning", "Data Analysis", "Android"]

predefined_skills = [
    "Python",
    "Django",
    "Flutter",
    "AI",
    "Machine Learning",
    "MySQL",
    "HTML",
    "CSS",
    "JavaScript",
    "React"
]
company = []

# predefined_skills, company = resume_skill()
# print("predefined_skills......", predefined_skills)

def extract_skills(text):

    if not predefined_skills:
        return []

    extracted_skills = []

    skill_pattern = r'\b(?:' + '|'.join(
        re.escape(skill) for skill in predefined_skills
    ) + r')\b'

    matches = re.findall(
        skill_pattern,
        text,
        flags=re.IGNORECASE
    )

    for match in matches:

        cleaned = match.strip()

        if cleaned:
            extracted_skills.append(cleaned.title())

    # Remove duplicates
    return list(set(extracted_skills))

def parse_pdf(pdf_path):

    skills = []

    pdf_reader = PdfReader(pdf_path)

    for page in pdf_reader.pages:

        text = page.extract_text()

        if text:
            skills += extract_skills(text)

    return list(set(skills))

# Function to parse Word document

def parse_word_doc(docx_path):

    skills = []

    doc = Document(docx_path)

    for paragraph in doc.paragraphs:

        text = paragraph.text

        skills += extract_skills(text)

    return list(set(skills))

# Function to parse a single resume

def parse_resume(resume_path):

    _, file_extension = os.path.splitext(resume_path)

    if file_extension.lower() == ".pdf":

        skills = parse_pdf(resume_path)

    elif file_extension.lower() == ".docx":

        skills = parse_word_doc(resume_path)

    else:

        raise ValueError("Unsupported file format")

    return list(set(skills))

# Function to process all resumes in a folder

def process_resumes_in_folder(folder_path):
    matching_skills_all_resumes = {}
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith((".pdf", ".docx")):
                resume_path = os.path.join(root, file)
                matching_skills = parse_resume(resume_path)
                matching_skills_all_resumes[resume_path] = matching_skills
                print('matching_skills_all_resumes',matching_skills_all_resumes)
    return matching_skills_all_resumes

#resume path
import json
def resumes(resume_file, user_instance):

    resume_path = resume_file.path

    matching_skills = parse_resume(resume_path)

    print("MATCHING SKILLS =", matching_skills)

    # Delete previous skills for this user
    tb_skill.objects.filter(user_id=user_instance).delete()

    # Save skills safely using JSON
    tb_skill.objects.create(
        user_id=user_instance,
        skill=json.dumps(matching_skills)
    )

    return matching_skills


def main():
    result = resumes()
    return result     



def user_view_notification(request):
    user_id = request.session.get('id')
    
    # Retrieve notifications from the database based on user_id
    notifications = tbl_notification.objects.filter(application__user__id=user_id)
    
    # Pass the notifications to the template
    context = {'notifications': notifications}
    
    # Render the template
    return render(request, 'user/user_view_notification.html', context)
