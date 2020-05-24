from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Profile, Prescription

# from .models import CustomUser

PROF = [('Patient', 'Patient',), ('Doctor', 'Doctor')]


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    '''PROF = forms.ChoiceField(required=True, widget=forms.RadioSelect(attrs={'class': 'Radio'}),
                             choices=(('Patient', 'Patient',), ('Doctor', 'Doctor')))
    role = forms.CharField(max_length=10)'''

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']  # 'PROF', 'role',

    '''def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.PROF = self.cleaned_data["PROF"]
        user.role = self.cleaned_data["role"]
        if commit:
            user.save()
            print('entered')
        print(user)
        return user'''


class UserRegistrationProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['prof']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['prof', 'gender', 'age', 'bloodGroup', 'phoneNumber', 'casePaper']


class CreatePrescription(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['symptoms', 'prescription']


'''class UserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'prof2']'''
