from django.contrib import admin
from django.urls import path
from . import views
from resumeapp import views
from .views import recruiter_jobviewmore

urlpatterns = [
path('',views.index, name='index'),
path('user_register/',views.user_register, name='user_register'),
path('recruiter_register/',views.recruiter_register, name='recruiter_register'),
path('login/',views.login,name='login'),
path('logout/',views.logout, name='logout'),




path('user_home/',views.user_home,name='user_home'),
path('user_viewprofile/', views.user_viewprofile, name='user_viewprofile'),
path('user_editprofile/', views.user_editprofile,name='user_editprofile'),
path('user_uploadresume/',views.user_uploadresume, name='user_uploadresume'),
path('user_view_jobs/',views.user_view_jobs,name='user_view_jobs'),
path('user_uploadresume/',views.user_uploadresume, name='user_uploadresume'),
# path('extract_skills/',views.extract_skills),
path('user_view_resume/', views.user_view_resume, name='user_view_resume'),
path('user_apply_job/<int:job_id>/', views.user_apply_job, name='user_apply_job'),
path('user_view_applied_jobs/', views.user_view_applied_jobs, name='user_view_applied_jobs'),
path('user_cancel_application/<int:appli_id>/', views.user_cancel_application, name='user_cancel_application'),
path('user_view_notification/', views.user_view_notification, name='user_view_notification'),
path('user_jobviewmore/<int:job_id>/', views.user_jobviewmore, name='user_jobviewmore'),


path('recruiter_home/',views.recruiter_home, name='recruiter_home'),
path('recruiter_addjob/', views.recruiter_addjob, name='recruiter_addjob'),
path('recruiter_viewjob/', views.recruiter_viewjob, name='recruiter_viewjob'),
path('recruiter_jobviewmore/<int:job_id>/', recruiter_jobviewmore, name='recruiter_jobviewmore'),
path('recruiter_viewprofile/', views.recruiter_viewprofile, name='recruiter_viewprofile'),
path('recruiter_editprofile/', views.recruiter_editprofile, name='recruiter_editprofile'),
path('resume_skill/<int:id>',views.resume_skill,name='resume_skill'),
path('recruiter_updatejob/<int:job_id>/',views.recruiter_updatejob, name='recruiter_updatejob'),
path('recruiter_deletejob/<int:job_id>/',views.recruiter_deletejob, name='recruiter_deletejob'),
path('recruiter_view_pending_applicants/',views.recruiter_view_pending_applicants, name='recruiter_view_pending_applicants'),
path('recruiter_view_rejected_applicants/',views.recruiter_view_rejected_applicants, name='recruiter_view_rejected_applicants'),
path('recruiter_view_shortlisted_applicants/',views.recruiter_view_shortlisted_applicants, name='recruiter_view_shortlisted_applicants'),

path('shortlistCandidate/<int:appli_id>/',views.shortlistCandidate, name='shortlistCandidate'),
path('rejectCandidate/<int:appli_id>/',views.rejectCandidate, name='rejectCandidate'),
path('recruiter_view_applicants/<int:job_id>/', views.recruiter_view_applicants, name='recruiter_view_applicants'),
  path('recruiter_create_notification/<int:appli_id>/', views.recruiter_create_notification, name='recruiter_create_notification'),







path('admin_home/',views.admin_home, name='admin_home'),
path('admin_viewpending/',views.admin_viewpending, name='admin_viewpending'),
path('admin_approve/<int:user_id>/', views.admin_approve, name='admin_approve'),
path('admin_reject/<int:user_id>/', views.admin_reject, name='admin_reject'),
path('admin_viewapproved/',views.admin_viewapproved, name='admin_viewapproved'),
path('admin_viewrecruiters/',views.admin_viewrecruiters, name='admin_viewrecruiters'),
path('admin_viewrejected/',views.admin_viewrejected, name='admin_viewrejected'),
path('admin_viewjob/<int:company_id>',views.admin_viewjob, name='admin_viewjob' ),
path('view_users/',views.view_users,name='view_users'),

path('main/',views.main, name='main' ),

path('process_resumes_in_folder/',views.process_resumes_in_folder, name='process_resumes_in_folder'),

path('parse_resume/',views.parse_resume, name='parse_resume'),
path('parse_word_doc/',views.parse_word_doc, name='parse_word_doc'),
path('parse_pdf/',views.parse_pdf, name='parse_pdf'),
path('extract_skills/',views.extract_skills, name='extract_skills'),
path('resumes/',views.resumes, name='resumes'),

]







from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)