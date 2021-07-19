from datetime import date
from pprint import pprint

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.core.serializers import serialize

from account.models import *

from jobapp.models import *
from jobapp.permission import *
from .forms import *


User = get_user_model()


def home_view(request):
    published_jobs = Job.objects.filter(is_published=True).order_by('-timestamp')
    jobs = published_jobs.filter(is_closed=False)
    total_candidates = User.objects.filter(role='employee').count()
    total_companies = User.objects.filter(role='employer').count()
    paginator = Paginator(jobs, 3)
    page_number = request.GET.get('page', None)
    page_obj = paginator.get_page(page_number)

    if request.is_ajax():
        job_lists = []
        job_objects_list = page_obj.object_list.values()
        for job_list in job_objects_list:
            job_lists.append(job_list)

        next_page_number = None
        if page_obj.has_next():
            next_page_number = page_obj.next_page_number()

        prev_page_number = None
        if page_obj.has_previous():
            prev_page_number = page_obj.previous_page_number()

        data = {
            'job_lists': job_lists,
            'current_page_no': page_obj.number,
            'next_page_number': next_page_number,
            'no_of_page': paginator.num_pages,
            'prev_page_number': prev_page_number
        }
        return JsonResponse(data)

    context = {

        'total_candidates': total_candidates,
        'total_companies': total_companies,
        'total_jobs': len(jobs),
        'total_completed_jobs': len(published_jobs.filter(is_closed=True)),
        'page_obj': page_obj
    }
    print('ok')
    return render(request, 'jobapp/index.html', context)


def job_list_View(request):
    """

    """
    job_list = Job.objects.filter(is_published=True, is_closed=False).order_by('-timestamp')
    paginator = Paginator(job_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {

        'page_obj': page_obj,

    }
    return render(request, 'jobapp/job-list.html', context)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def create_job_View(request):
    """
    Provide the ability to create job post
    """
    form = JobForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)
    categories = Category.objects.all()

    if request.method == 'POST':

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.save()
            # for save tags
            form.save_m2m()
            messages.success(
                request, 'You are successfully posted your job! Please wait for review.')
            return redirect(reverse("jobapp:single-job", kwargs={
                'id': instance.id
            }))

    context = {
        'form': form,
        'categories': categories
    }
    return render(request, 'jobapp/post-job.html', context)


def single_job_view(request, id):
    """
    Provide the ability to view job details
    """

    job = get_object_or_404(Job, id=id)
    mainCV = cv.objects.filter(default=True).get()

    related_job_list = job.tags.similar_objects()

    paginator = Paginator(related_job_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'job': job,
        'page_obj': page_obj,
        'total': len(related_job_list),
        'mainCV': mainCV,

    }
    return render(request, 'jobapp/job-single.html', context)


def search_result_view(request):
    """
        User can search job with multiple fields

    """

    job_list = Job.objects.order_by('-timestamp')

    # Keywords
    if 'job_title_or_company_name' in request.GET:
        job_title_or_company_name = request.GET['job_title_or_company_name']

        if job_title_or_company_name:
            job_list = job_list.filter(title__icontains=job_title_or_company_name) | job_list.filter(
                company_name__icontains=job_title_or_company_name)

    # location
    if 'location' in request.GET:
        location = request.GET['location']
        if location:
            job_list = job_list.filter(location__icontains=location)

    # Job Type
    if 'job_type' in request.GET:
        job_type = request.GET['job_type']
        if job_type:
            job_list = job_list.filter(job_type__iexact=job_type)

    # job_title_or_company_name = request.GET.get('text')
    # location = request.GET.get('location')
    # job_type = request.GET.get('type')

    #     job_list = Job.objects.all()
    #     job_list = job_list.filter(
    #         Q(job_type__iexact=job_type) |
    #         Q(title__icontains=job_title_or_company_name) |
    #         Q(location__icontains=location)
    #     ).distinct()

    # job_list = Job.objects.filter(job_type__iexact=job_type) | Job.objects.filter(
    #     location__icontains=location) | Job.objects.filter(title__icontains=text) | Job.objects.filter(company_name__icontains=text)

    paginator = Paginator(job_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {

        'page_obj': page_obj,

    }
    return render(request, 'jobapp/result.html', context)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def apply_job_view(request, id):
    form = JobApplyForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)

    mainCV = cv.objects.filter(user=request.user.id, default=True).get()

    applicant = Applicant.objects.filter(user=user, job=id)
    print(mainCV.__dict__)

    if not applicant:
        if request.method == 'POST':
            if 'apply' in request.POST:
                if form.is_valid():
                    instance = form.save(commit=False)
                    instance.user = user
                    instance.cv_id = mainCV.id
                    instance.save()

                    messages.success(
                        request, 'You have successfully applied for this job!')
                    return redirect(reverse("jobapp:single-job", kwargs={
                        'id': id
                    }))
    if applicant:
            if 'unapply' in request.POST:
                if form.is_valid():

                    job = Applicant.objects.get(user=user.id, job=id)
                    job.delete()
                    messages.success(
                        request, 'You have successfully delete your application for this job!')
                    return redirect(reverse("jobapp:single-job", kwargs={
                        'id': id
                    }))




            return redirect(reverse("jobapp:single-job", kwargs={
                'id': id
            }))

    else:

        messages.error(request, 'You already applied for the Job!')

        return redirect(reverse("jobapp:single-job", kwargs={
            'id': id
        }))


@login_required(login_url=reverse_lazy('account:login'))
def dashboard_view(request):
    """
    """
    jobs = []
    savedjobs = []
    appliedjobs = []
    total_applicants = {}

    user = get_object_or_404(User, id=request.user.id)
    today = date.today()
    if user.role == 'employee':
        bday = today.year - user.date_of_birth.year - (
                (today.month, today.day) < (user.date_of_birth.month, user.date_of_birth.day))

    cvs = cv.objects.filter(user = request.user.id)

    print(user.__dict__)
    print(cvs.__dict__)
    if request.user.role == 'employer':

        jobs = Job.objects.filter(user=request.user.id)
        for job in jobs:
            count = Applicant.objects.filter(job=job.id).count()
            total_applicants[job.id] = count

    if request.user.role == 'employee':
        cvs = cv.objects.filter(user=request.user.id)
        savedjobs = BookmarkJob.objects.filter(user=request.user.id)
        appliedjobs = Applicant.objects.filter(user=request.user.id)

        context = {
            'bday': bday,
            'user': user,
            'jobs': jobs,
            'savedjobs': savedjobs,
            'appliedjobs': appliedjobs,
            'total_applicants': total_applicants,
            'cvs': cvs
        }
    else:
        context = {

            'user': user,
            'jobs': jobs,
            'savedjobs': savedjobs,
            'appliedjobs': appliedjobs,
            'total_applicants': total_applicants
        }
    return render(request, 'jobapp/dashboard.html', context)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def delete_job_view(request, id):
    job = get_object_or_404(Job, id=id, user=request.user.id)

    if job:
        job.delete()
        messages.success(request, 'Your Job Post was successfully deleted!')

    return redirect('jobapp:dashboard')


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def make_complete_job_view(request, id):
    job = get_object_or_404(Job, id=id, user=request.user.id)

    if job:
        try:
            job.is_closed = True
            job.save()
            messages.success(request, 'Your Job was marked closed!')
        except:
            messages.success(request, 'Something went wrong !')

    return redirect('jobapp:dashboard')


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def all_applicants_view(request, id):
    all_applicants = Applicant.objects.filter(job=id)

    context = {

        'all_applicants': all_applicants
    }

    return render(request, 'jobapp/all-applicants.html', context)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def delete_bookmark_view(request, id):
    job = get_object_or_404(BookmarkJob, id=id, user=request.user.id)

    if job:
        job.delete()
        messages.success(request, 'Saved Job was successfully deleted!')

    return redirect('jobapp:dashboard')


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def applicant_details_view(request, id):
    applicant = get_object_or_404(User, id=id)

    context = {

        'applicant': applicant
    }

    return render(request, 'jobapp/applicant-details.html', context)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def job_bookmark_view(request, id):
    form = JobBookmarkForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)
    applicant = BookmarkJob.objects.filter(user=request.user.id, job=id)

    if not applicant:
        if request.method == 'POST':

            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.save()

                messages.success(
                    request, 'You have successfully save this job!')
                return redirect(reverse("jobapp:single-job", kwargs={
                    'id': id
                }))

        else:
            return redirect(reverse("jobapp:single-job", kwargs={
                'id': id
            }))

    else:
        messages.error(request, 'You already saved this Job!')

        return redirect(reverse("jobapp:single-job", kwargs={
            'id': id
        }))


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def job_edit_view(request, id=id):
    """
    Handle Employee Profile Update

    """

    job = get_object_or_404(Job, id=id)
    categories = Category.objects.all()
    form = JobEditForm(request.POST or None, instance=job)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        # for save tags
        # form.save_m2m()
        messages.success(request, 'Your Job Post Was Successfully Updated!')
        return redirect(reverse("jobapp:single-job", kwargs={
            'id': instance.id
        }))
    context = {

        'form': form,
        'categories': categories
    }

    return render(request, 'jobapp/job-edit.html', context)


def employer_edit_profile(request, id=id):
    """
    Handle Employee Profile Update Functionality

    """

    user = get_object_or_404(User, id=id)
    form = EmployerProfileEditForm(request.POST or None, request.FILES or None, instance=user)
    if form.is_valid():
        form = form.save()
        messages.success(request, 'Your Company Profile Was Successfully Updated!')
        return redirect(reverse("jobapp:employer-edit-profile", kwargs={
            'id': form.id
        }))
    context = {

        'form': form
    }

    return render(request, 'account:employee-edit-profile.html', context)


def addNewCv(request, id=id):
    # form = JobForm(request.POST or None)
    #
    # user = get_object_or_404(User, id=request.user.id)
    # categories = Category.objects.all()
    #
    # if request.method == 'POST':
    #
    #     if form.is_valid():
    #         instance = form.save(commit=False)
    #         instance.user = user
    #         instance.save()
    #         # for save tags
    #         form.save_m2m()
    #         messages.success(
    #             request, 'You are successfully posted your job! Please wait for review.')
    #         return redirect(reverse("jobapp:single-job", kwargs={
    #             'id': instance.id
    #         }))
    #
    # context = {
    #     'form': form,
    #     'categories': categories
    # }
    # return render(request, 'jobapp/post-job.html', context)

    return render(request, 'jobapp/cv-form.html')


def addCv(request):
    form = cvForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)

    if request.method == 'POST':

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.save()
            # for save tags
            form.save_m2m()
            messages.success(request, 'You are successfully named the title of your cv .')
            return redirect(reverse("jobapp:newExperiance", kwargs={
                'id': instance.id
            }))
            # return render(request, 'jobapp/dashboard.html')




    context = {
        'form': form,
        'user': user,

    }

    return render(request, 'jobapp/newcv.html', context)


def addnewExperiance(request, id=id):
    cvs = cv.objects.get(pk=id)
    form = addExperianceForm(request.POST or None)
    tosend = int(cvs.id)
    user = get_object_or_404(User, id=request.user.id)

    if request.method == 'POST':

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.cv = cvs
            instance.save()
            # for save tags
            form.save_m2m()
            messages.success(request, 'You are successfully added new experience .')
            return redirect(reverse("jobapp:newFormation", kwargs={
                'id': tosend
            }))

    context = {
        'form': form,
        'cv': cvs,
        'user': user,

    }

    return render(request, 'jobapp/addexperiance.html',context)


def addnewFormation(request, id=id):

    cvs = cv.objects.get(pk=id)

    form = addnewFormationForm(request.POST or None)




    user = get_object_or_404(User, id=request.user.id)


    if request.method == 'POST':

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.cv = cvs
            instance.save()
            # for save tags
            form.save_m2m()
            messages.success(request, 'You are successfully added new experience .')
            return redirect(reverse("jobapp:newSkill", kwargs={
                'id': cvs.id
            }))

    context = {
        'form': form,

        'user': user,

    }

    return render(request, 'jobapp/addFormation.html',context)


def addnewSkill(request, id=id):

    cvs = cv.objects.get(pk=id)

    form = addSkillForm(request.POST or None)




    user = get_object_or_404(User, id=request.user.id)


    if request.method == 'POST':

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.cv = cvs
            instance.save()
            # for save tags
            form.save_m2m()
            messages.success(request, 'You are successfully added new experience .')
            return redirect(reverse("jobapp:cvCompleted", kwargs={
                'id': cvs.id
            }))

    context = {
        'form': form,

        'user': user,

    }

    return render(request, 'jobapp/addskills.html',context)


def cvCompleted(request, id=id):

    user = get_object_or_404(User, id=request.user.id)
    context = {

        'user': user,

    }

    return render(request, 'jobapp/cvcompleted.html', context)


def addnewExperiancedashboard(request, id=id):
    cvs = cv.objects.get(name=id)
    form = addExperianceForm(request.POST or None)
    tosend = int(cvs.id)
    user = get_object_or_404(User, id=request.user.id)

    if request.method == 'POST':

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.cv = cvs
            instance.save()
            # for save tags
            form.save_m2m()
            messages.success(request, 'You are successfully added new experience .')
            return redirect(reverse("jobapp:dashboard"))

    context = {
        'form': form,
        'cv': cvs,
        'user': user,

    }

    return render(request, 'jobapp/addNewExperience.html',context)

def addnewFormationdashboard(request, id=id):

    cvs = cv.objects.get(name=id)

    form = addnewFormationForm(request.POST or None)




    user = get_object_or_404(User, id=request.user.id)


    if request.method == 'POST':

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.cv = cvs
            instance.save()
            # for save tags
            form.save_m2m()
            messages.success(request, 'You are successfully added new experience .')
            return redirect(reverse("jobapp:dashboard"))

    context = {
        'form': form,

        'user': user,

    }

    return render(request, 'jobapp/addNewFormation.html',context)

def addnewSkilldashboard(request, id=id):

    cvs = cv.objects.get(name=id)

    form = addSkillForm(request.POST or None)




    user = get_object_or_404(User, id=request.user.id)


    if request.method == 'POST':

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.cv = cvs
            instance.save()
            # for save tags
            form.save_m2m()
            messages.success(request, 'You are successfully added new experience .')
            return redirect(reverse("jobapp:dashboard"))

    context = {
        'form': form,

        'user': user,

    }

    return render(request, 'jobapp/addNewSkill.html',context)


def makeDefault(request,id=id):

    cv.objects.all().update(default= False)
    cvs = cv.objects.get(name=id)
    cvs.default = True
    cvs.save()

    return redirect(reverse("jobapp:dashboard"))