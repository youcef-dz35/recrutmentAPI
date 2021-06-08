from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from account.models import User
from account.models import Experience


class EmployeeExperienceForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        UserCreationForm.__init__(self, *args, **kwargs)

        self.fields['name'].label = "name   :"
        self.fields['date_debut'].label = "Date debut :"
        self.fields['date_fin'].label = "Date fin :"
        self.fields['poste'].label = "Poste :"
        self.fields['fonction'].label = "Fonction :"
        self.fields['entreprise'].label = "Entreprise :"
        self.fields['type_entreprise'].label = "Type_entreprise :"
        self.fields['description_deposte'].label = "Description_deposte :"

        self.fields['name'].widget.attrs.update(
            {
                'placeholder': 'Enter Name',
            }
        )
        self.fields['date_debut'].widget.attrs.update(
            {
                'placeholder': 'Date debut',
            }
        )
        self.fields['date_fin'].widget.attrs.update(
            {
                'placeholder': 'Enter date fin',
            }
        )
        self.fields['poste'].widget.attrs.update(
            {
                'placeholder': 'poste',
            }
        )
        self.fields['fonction'].widget.attrs.update(
            {
                'placeholder': 'Fonction',
            }
        )
        self.fields['entreprise'].widget.attrs.update(
            {
                'placeholder': 'Enter entreprise',

            }
        )
        self.fields['type_entreprise'].widget.attrs.update(
            {
                'placeholder': 'type entreprise',
            }
        )
        self.fields['description_deposte'].widget.attrs.update(
            {
                'placeholder': 'descritpion de poste',
            }
        )

    class Meta:

        model = Experience

        fields = ['name', 'date_debut', 'date_fin', 'poste', 'fonction', 'entreprise', 'type_entreprise',
                  'description_deposte']

    def clean_gender(self):
        gender = self.cleaned_data.get('gender')
        if not gender:
            raise forms.ValidationError("Gender is required")
        return gender

    def save(self, commit=True):
        user = UserCreationForm.save(self, commit=False)
        user.role = "employee"
        if commit:
            user.save()
        return user


class EmployerRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        UserCreationForm.__init__(self, *args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['first_name'].label = "Company Name"
        self.fields['last_name'].label = "Company Address"
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Confirm Password"
        self.fields['telephone'].label = "Telephone :"
        self.fields['zip_code'].label = "Zip code :"
        self.fields['city'].label = "City :"

        self.fields['first_name'].widget.attrs.update(
            {
                'placeholder': 'Enter Company Name',
            }
        )
        self.fields['last_name'].widget.attrs.update(
            {
                'placeholder': 'Enter Company Address',
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'placeholder': 'Enter Email',
            }
        )

        self.fields['telephone'].widget.attrs.update(
            {
                'placeholder': 'Phone Number',
            }
        )

        self.fields['city'].widget.attrs.update(
            {
                'placeholder': 'city where the company resides',
            }
        )
        self.fields['zip_code'].widget.attrs.update(
            {
                'placeholder': 'Zip Code',
            }
        )
        self.fields['password1'].widget.attrs.update(
            {
                'placeholder': 'Enter Password',
            }
        )
        self.fields['password2'].widget.attrs.update(
            {
                'placeholder': 'Confirm Password',
            }
        )

    class Meta:
        model = User

        fields = ['first_name', 'last_name', 'email', 'password1', 'password2', 'telephone', 'city', 'zip_code']

    def save(self, commit=True):
        user = UserCreationForm.save(self, commit=False)
        user.role = "employer"
        if commit:
            user.save()
        return user


class EmployerRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        UserCreationForm.__init__(self, *args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['first_name'].label = "Company Name"
        self.fields['last_name'].label = "Company Address"
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Confirm Password"
        self.fields['telephone'].label = "Telephone :"
        self.fields['zip_code'].label = "Zip code :"
        self.fields['city'].label = "City :"

        self.fields['first_name'].widget.attrs.update(
            {
                'placeholder': 'Enter Company Name',
            }
        )
        self.fields['last_name'].widget.attrs.update(
            {
                'placeholder': 'Enter Company Address',
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'placeholder': 'Enter Email',
            }
        )

        self.fields['telephone'].widget.attrs.update(
            {
                'placeholder': 'Phone Number',
            }
        )

        self.fields['city'].widget.attrs.update(
            {
                'placeholder': 'city where the company resides',
            }
        )
        self.fields['zip_code'].widget.attrs.update(
            {
                'placeholder': 'Zip Code',
            }
        )
        self.fields['password1'].widget.attrs.update(
            {
                'placeholder': 'Enter Password',
            }
        )
        self.fields['password2'].widget.attrs.update(
            {
                'placeholder': 'Confirm Password',
            }
        )

    class Meta:
        model = User

        fields = ['first_name', 'last_name', 'email', 'password1', 'password2', 'telephone', 'city', 'zip_code']

    def save(self, commit=True):
        user = UserCreationForm.save(self, commit=False)
        user.role = "employer"
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email', })
    )
    password = forms.CharField(strip=False, widget=forms.PasswordInput(attrs={

        'placeholder': 'Password',
    }))

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user = authenticate(email=email, password=password)
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise forms.ValidationError("User Does Not Exist.")

            if not user.check_password(password):
                raise forms.ValidationError("Password Does not Match.")

            if not user.is_active:
                raise forms.ValidationError("User is not Active.")

        return super(UserLoginForm, self).clean(*args, **kwargs)

    def get_user(self):
        return self.user


class EmployeeProfileEditForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EmployeeProfileEditForm, self).__init__(*args, **kwargs)
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
        self.fields['operate'].widget.attrs.update(
            {
                'placeholder': 'by switching this your profile will no longer be accessible',
            }
        )

        self.fields['civil'].widget.attrs.update(
            {
                'placeholder': 'Civil Status',
            }
        )
        self.fields['telephone'].widget.attrs.update(
            {
                'placeholder': 'Phone Number',
            }
        )
        self.fields['date_of_birth'].widget.attrs.update(
            {
                'placeholder': 'Enter your Date Of Birth',

            }
        )
        self.fields['address'].widget.attrs.update(
            {
                'placeholder': 'Enter your address',
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
                'placeholder': 'Your Profile Picture ',
            }
        )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "gender", 'civil', 'telephone', 'date_of_birth', 'address', 'zip_code',
                  'city', 'operate', 'image']
