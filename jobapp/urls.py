from django.urls import path
from jobapp import views

app_name = "jobapp"


urlpatterns = [

    path('', views.home_view, name='home'),
    path('jobs/', views.job_list_View, name='job-list'),
    path('job/create/', views.create_job_View, name='create-job'),
    path('job/<int:id>/', views.single_job_view, name='single-job'),
    path('apply-job/<int:id>/', views.apply_job_view, name='apply-job'),
    path('bookmark-job/<int:id>/', views.job_bookmark_view, name='bookmark-job'),
    path('about/', views.single_job_view, name='about'),
    path('contact/', views.single_job_view, name='contact'),
    path('result/', views.search_result_view, name='search_result'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/employer/job/<int:id>/applicants/', views.all_applicants_view, name='applicants'),

    path('dashboard/employer/job/edit/<int:id>', views.job_edit_view, name='edit-job'),
    path('dashboard/employer/applicant/<int:id>/', views.applicant_details_view, name='applicant-details'),
    path('dashboard/employer/close/<int:id>/', views.make_complete_job_view, name='complete'),
    path('dashboard/employer/delete/<int:id>/', views.delete_job_view, name='delete'),
    path('dashboard/employee/delete-bookmark/<int:id>/', views.delete_bookmark_view, name='delete-bookmark'),
    path('employer/profile/edit/<int:id>/', views.employer_edit_profile, name='employer-edit-profile'), #must be verified later


    path('employee/addCv/<int:id>/', views.addNewCv, name='addCV'),
    path('employee/newCv/', views.addCv, name='newCV'),
    path('employee/newCv/addExperiance/<int:id>/', views.addnewExperiance, name='newExperiance'),
    path('employee/matchWithRecruter/<int:id>/', views.matchRecruter, name='matchRecruter'),
    path('employee/recruterValidation/', views.passwordVerification, name='passwordVerification'),

    path('employee/newCv/addFormation/<int:id>/', views.addnewFormation, name='newFormation'),
    path('employee/newCv/addskills/<int:id>/', views.addnewSkill, name='newSkill'),
    path('employee/newCv/cvCompleted/<int:id>/', views.cvCompleted, name='cvCompleted'),
    path('employee/newCv/addNewExperience/<str:id>/', views.addnewExperiancedashboard, name='addNewExperience'),
    path('employee/newCv/addNewFormation/<str:id>/', views.addnewFormationdashboard, name='addNewFormation'),
    path('employee/newCv/addNewCompetance/<str:id>/', views.addnewSkilldashboard, name='addNewSkill'),
    path('employee/newCv/makedefault/<str:id>/', views.makeDefault, name='makeDefault'),


]
