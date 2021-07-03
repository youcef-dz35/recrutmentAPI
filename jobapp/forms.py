import datetime

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib import auth

from jobapp.models import *
from account.models import *
from ckeditor.widgets import CKEditorWidget





class JobForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['title'].label = "Job Title :"
        self.fields['location'].label = "Job Location :"
        self.fields['salary'].label = "Salary :"
        self.fields['description'].label = "Job Description :"
        self.fields['tags'].label = "Tags :"
        self.fields['last_date'].label = "Submission Deadline :"
        self.fields['company_name'].label = "Company Name :"
        self.fields['url'].label = "Website :"

        self.fields['title'].widget.attrs.update(
            {
                'placeholder': 'eg : Software Developer',
            }
        )
        self.fields['location'].widget.attrs.update(
            {
                'placeholder': 'eg : Bangladesh',
            }
        )
        self.fields['salary'].widget.attrs.update(
            {
                'placeholder': '$800 - $1200',
            }
        )
        self.fields['tags'].widget.attrs.update(
            {
                'placeholder': 'Use comma separated. eg: Python, JavaScript ',
            }
        )
        self.fields['last_date'].widget.attrs.update(
            {
                'placeholder': 'YYYY-MM-DD ',

            }
        )
        self.fields['company_name'].widget.attrs.update(
            {
                'placeholder': 'Company Name',
            }
        )
        self.fields['url'].widget.attrs.update(
            {
                'placeholder': 'https://example.com',
            }
        )

    class Meta:
        model = Job

        fields = [
            "title",
            "location",
            "job_type",
            "category",
            "salary",
            "description",
            "tags",
            "last_date",
            "company_name",
            "company_description",
            "url"
        ]

    def clean_job_type(self):
        job_type = self.cleaned_data.get('job_type')

        if not job_type:
            raise forms.ValidationError("Service is required")
        return job_type

    def clean_category(self):
        category = self.cleaned_data.get('category')

        if not category:
            raise forms.ValidationError("category is required")
        return category

    def save(self, commit=True):
        job = super(JobForm, self).save(commit=False)
        if commit:
            user.save()
        return job


class JobApplyForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ['job']


class JobBookmarkForm(forms.ModelForm):
    class Meta:
        model = BookmarkJob
        fields = ['job']


class JobEditForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['title'].label = "Job Title :"
        self.fields['location'].label = "Job Location :"
        self.fields['salary'].label = "Salary :"
        self.fields['description'].label = "Job Description :"
        # self.fields['tags'].label = "Tags :"
        self.fields['last_date'].label = "Dead Line :"
        self.fields['company_name'].label = "Company Name :"
        self.fields['url'].label = "Website :"

        self.fields['title'].widget.attrs.update(
            {
                'placeholder': 'eg : Software Developer',
            }
        )
        self.fields['location'].widget.attrs.update(
            {
                'placeholder': 'eg : Bangladesh',
            }
        )
        self.fields['salary'].widget.attrs.update(
            {
                'placeholder': '$800 - $1200',
            }
        )
        # self.fields['tags'].widget.attrs.update(
        #     {
        #         'placeholder': 'Use comma separated. eg: Python, JavaScript ',
        #     }
        # )                        
        self.fields['last_date'].widget.attrs.update(
            {
                'placeholder': 'YYYY-MM-DD ',
            }
        )
        self.fields['company_name'].widget.attrs.update(
            {
                'placeholder': 'Company Name',
            }
        )
        self.fields['url'].widget.attrs.update(
            {
                'placeholder': 'https://example.com',
            }
        )

        last_date = forms.CharField(widget=forms.TextInput(attrs={
            'placeholder': 'Service Name',
            'class': 'datetimepicker1'
        }))

    class Meta:
        model = Job

        fields = [
            "title",
            "location",
            "job_type",
            "category",
            "salary",
            "description",
            "last_date",
            "company_name",
            "company_description",
            "url"
        ]

    def clean_job_type(self):
        job_type = self.cleaned_data.get('job_type')

        if not job_type:
            raise forms.ValidationError("Service is required")
        return job_type

    def clean_category(self):
        category = self.cleaned_data.get('category')

        if not category:
            raise forms.ValidationError("category is required")
        return category

    def save(self, commit=True):
        job = super(JobEditForm, self).save(commit=False)
        if commit:
            user.save()
        return job


class EmployerProfileEditForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EmployerProfileEditForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update(
            {
                'placeholder': 'Enter First Name',
            }
        )
        self.fields['last_name'].widget.attrs.update(
            {
                'placeholder': 'Enter Last Name',
            }
        )

        self.fields['telephone'].widget.attrs.update(
            {
                'placeholder': 'Phone Number',
            }
        )

        self.fields['zip_code'].widget.attrs.update(
            {
                'placeholder': 'Zip Code',
            }
        )
        self.fields['city'].widget.attrs.update(
            {
                'placeholder': 'city of habitat',
            }
        )
        self.fields['image'].widget.attrs.update(
            {
                'placeholder': 'Your Company LOGO ',
            }
        )

    class Meta:
        model = User
        fields = ["first_name", "last_name", 'telephone', 'zip_code', 'city', 'image']


class AddCV(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['entryDate'].label = "Entry date "
        self.fields['finishDate'].label = "Finish date "
        self.fields['jobTitle'].label = "Job title "
        self.fields['field'].label = "Field "
        self.fields['enterpriseName'].label = "Enterprise name"
        self.fields['enterpriseType'].label = "Enterprise type "
        self.fields['activitySector'].label = "Activity sector "
        self.fields['jobDescription'].label = "Job description "
        # first slide is done
        # now the second slide will start
        self.fields['formationFinishDate'].label = "finish date "
        self.fields['domain'].label = "Domain "
        self.fields['formationType'].label = "Type "
        self.fields['studies'].label = "highest level of studies "
        self.fields['formationDescription'].label = "Description :"
        self.fields['cvPdf'].label = "CV :"
        self.fields['skills'].label = "Skills :"

        self.fields['entryDate'].widget.attrs.update(
            {
                'placeholder': 'Entry Date',
            }
        )
        self.fields['finishDate'].widget.attrs.update(
            {
                'placeholder': 'Finish Date',
            }
        )
        self.fields['jobTitle'].widget.attrs.update(
            {
                'placeholder': 'Job Title',
            }
        )
        self.fields['field'].widget.attrs.update(
            {
                'placeholder': 'field',
            }
        )
        self.fields['enterpriseName'].widget.attrs.update(
            {
                'placeholder': 'Enterprise Name',
            }
        )
        self.fields['enterpriseType'].widget.attrs.update(
            {
                'placeholder': 'Enterprise Type',
            }
        )
        self.fields['activitySector'].widget.attrs.update(
            {
                'placeholder': 'Activity Sector',
            }
        )
        self.fields['jobDescription'].widget.attrs.update(
            {
                'placeholder': 'Job Description',
            }
        )
        self.fields['formationFinishDate'].widget.attrs.update(
            {
                'placeholder': 'Formation Finish Date ',
            }
        )
        self.fields['studies'].widget.attrs.update(
            {
                'placeholder': 'Highest level of studies you accomplished ',

            }
        )
        self.fields['formationDescription'].widget.attrs.update(
            {
                'placeholder': 'Formation Description',
            }
        )
        self.fields['cvPdf'].widget.attrs.update(
            {
                'placeholder': 'Upload CV',
            }
        )
        self.fields['skills'].widget.attrs.update(
            {
                'placeholder': 'Upload CV',
            }
        )

    class Meta:
        model = Job

        fields = [
            "title",
            "location",
            "job_type",
            "category",
            "salary",
            "description",
            "tags",
            "last_date",
            "company_name",
            "company_description",
            "url"
        ]

    def clean_job_type(self):
        job_type = self.cleaned_data.get('job_type')

        if not job_type:
            raise forms.ValidationError("Service is required")
        return job_type

    def clean_category(self):
        category = self.cleaned_data.get('category')

        if not category:
            raise forms.ValidationError("category is required")
        return category

    def save(self, commit=True):
        job = super(JobForm, self).save(commit=False)
        if commit:
            user.save()
        return job


class cvForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['name'].label = "Enter your cv title "

    class Meta:
        model = cv
        fields = [
            "name",

        ]

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if not name:
            raise forms.ValidationError("The CV name is required")
        return name

    def save(self, commit=True):
        cv = super(cvForm, self).save(commit=False)
        if commit:
            cv.save()
        return cv


class addExperianceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['date_debut'].label = "Entry date "
        self.fields['date_fin'].label = "Finish date "
        self.fields['poste'].label = "Job title "
        self.fields['fonction'].label = "Field of work"
        self.fields['entreprise'].label = "Enterprise name"
        self.fields['type_entreprise'].label = "Enterprise type "
        self.fields['description_deposte'].label = "Job description "

        self.fields['date_debut'].widget.attrs.update(
            {
                'placeholder': 'Entry Date',
            }
        )
        self.fields['date_fin'].widget.attrs.update(
            {
                'placeholder': 'Finish Date',
            }
        )
        self.fields['poste'].widget.attrs.update(
            {
                'placeholder': 'Job Title',
            }
        )
        self.fields['fonction'].widget.attrs.update(
            {
                'placeholder': 'field',
            }
        )
        self.fields['entreprise'].widget.attrs.update(
            {
                'placeholder': 'Enterprise Name',
            }
        )
        self.fields['type_entreprise'].widget.attrs.update(
            {
                'placeholder': 'Enterprise Type',
            }
        )
        self.fields['description_deposte'].widget.attrs.update(
            {
                'placeholder': 'describe what were your missions in a short paragraph',
            }
        )

    class Meta:
        model = Experience
        fields = [
            "date_debut",
            "date_fin",
            "poste",
            "fonction",
            "entreprise",
            "type_entreprise",
            "description_deposte",

        ]

    def clean_date_debut(self):
        date_debut = self.cleaned_data.get('date_debut')

        if not date_debut:
            raise forms.ValidationError("The experience date must be filled")
        if date_debut > datetime.date.today():
            raise forms.ValidationError("starting  date cannot be later than today.")
        return date_debut

    def clean_date_fin(self):
        date_fin = self.cleaned_data.get('date_fin')
        date_debut = self.cleaned_data.get('date_debut')

        if not date_fin:
            raise forms.ValidationError("The experience date must be filled")
        if date_fin > datetime.date.today():
            raise forms.ValidationError("starting  date cannot be later than today.")
        if date_fin < date_debut:
            raise forms.ValidationError("finish date cannot be later than starting date.")
        return date_fin

    def clean_title(self):
        poste = self.cleaned_data.get('poste')

        if not poste:
            raise forms.ValidationError("Job Title is required")
        return poste

    def save(self, commit=True):
        experience = super(addExperianceForm, self).save(commit=False)
        if commit:
            experience.save()
        return experience


class addnewFormationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['date_debut'].label = "Entry date "
        self.fields['date_fin'].label = "Finish date "
        self.fields['domain'].label = "Domain of Internship "
        self.fields['type'].label = "Type  of Internship"
        self.fields['etude'].label = "Title of Diploma"
        self.fields['ecole'].label = "Institution "
        self.fields['description'].label = " Description"

        self.fields['date_debut'].widget.attrs.update(
            {
                'placeholder': 'Entry Date',
            }
        )
        self.fields['date_fin'].widget.attrs.update(
            {
                'placeholder': 'Finish Date',
            }
        )
        self.fields['domain'].widget.attrs.update(
            {
                'placeholder': 'Domain of Internship',
            }
        )
        self.fields['type'].widget.attrs.update(
            {
                'placeholder': 'Type  of Internship',
            }
        )
        self.fields['etude'].widget.attrs.update(
            {
                'placeholder': 'Title of Diploma',
            }
        )
        self.fields['ecole'].widget.attrs.update(
            {
                'placeholder': 'Institution where you studied',
            }
        )
        self.fields['description'].widget.attrs.update(
            {
                'placeholder': 'Brief description about the skills you achieved',
            }
        )

    class Meta:
        model = Formation
        fields = [
            "date_debut",
            "date_fin",
            "domain",
            "type",
            "etude",
            "ecole",
            "description",

        ]

    def clean_date_debut(self):
        date_debut = self.cleaned_data.get('date_debut')

        if not date_debut:
            raise forms.ValidationError("The Formation date must be filled")
        if date_debut > datetime.date.today():
            raise forms.ValidationError("starting  date cannot be later than today.")
        return date_debut

    def clean_date_fin(self):
        date_fin = self.cleaned_data.get('date_fin')
        date_debut = self.cleaned_data.get('date_debut')

        if not date_fin:
            raise forms.ValidationError("The Formation date must be filled")
        if date_fin > datetime.date.today():
            raise forms.ValidationError("starting  date cannot be later than today.")
        if date_fin < date_debut:
            raise forms.ValidationError("finish date cannot be later than starting date.")
        return date_fin

    def clean_domain(self):
        domain = self.cleaned_data.get('domain')

        if not domain:
            raise forms.ValidationError("domain is required")
        return domain

    def clean_type(self):
        type = self.cleaned_data.get('type')

        if not type:
            raise forms.ValidationError("type is required")
        return type

    def clean_etude(self):
        etude = self.cleaned_data.get('etude')

        if not etude:
            raise forms.ValidationError("formation title is required")
        return etude

    def clean_ecole(self):
        ecole = self.cleaned_data.get('ecole')

        if not ecole:
            raise forms.ValidationError("Institution is required")
        return ecole

    def save(self, commit=True):
        formation = super(addnewFormationForm, self).save(commit=False)
        if commit:
            formation.save()
        return formation


class addSkillForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['competence'].label = "please add your skills "

        self.fields['competence'].widget.attrs.update(
            {
                'placeholder': ' add skills here  ',
            }
        )

    class Meta:
        model = Competence
        fields = [
            "competence",


        ]

    def save(self, commit=True):
        competence = super(addSkillForm, self).save(commit=False)
        if commit:
            competence.save()
        return competence


