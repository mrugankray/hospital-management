from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm
from django.contrib.auth.models import User
from .forms import UserUpdateForm, ProfileUpdateForm, UserRegistrationProfileForm, CreatePrescription
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)
from .models import Prescription, Profile


# Create your views here.
def register(req):
    if req.method == 'POST':
        form = UserRegistrationForm(req.POST)
        rp_form = UserRegistrationProfileForm(req.POST)
        if form.is_valid() and rp_form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            rp_form = UserRegistrationProfileForm(req.POST, instance=user.profile)
            rp_form.full_clean()
            rp_form.save()
            form_data = form.cleaned_data
            '''user = User(username=form_data['username'], prof2=form_data['PROF'], email=form_data['email'],
                                password1=form_data['password1'])
            user.save()'''
            return redirect('login')
    else:
        form = UserRegistrationForm()
        rp_form = UserRegistrationProfileForm()

        context = {
            'form': form,
            'rp_form': rp_form
        }

    return render(req, 'users/register.html', context)


@login_required()
def profile(req):
    if req.method == 'POST':
        u_form = UserUpdateForm(req.POST, instance=req.user)
        p_form = ProfileUpdateForm(req.POST, instance=req.user.profile)
        if p_form.is_valid() and u_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=req.user)
        p_form = ProfileUpdateForm(instance=req.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(req, 'users/profile.html', context)


def home(req):
    return render(req, 'users/home.html')


def about(req):
    return render(req, 'users/about.html')


def is_doc(user):
    if user.profile.prof == 'Doctor':
        return True
    else:
        return False


def is_patient(user):
    if user.profile.prof == 'Patient':
        return True
    else:
        return False


@login_required()
@user_passes_test(is_doc)
def create_prescription(req):
    patient_list = Profile.objects.all().filter(prof='Patient')
    if req.method == 'POST':
        form = CreatePrescription(req.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            patient_username = req.POST.get('patient_username')
            doc_name = req.user
            user = User.objects.all().filter(username=patient_username).first()
            patient_first_name = user.first_name
            patient_last_name = user.last_name
            full_name = patient_first_name + ' ' + patient_last_name
            prescription = Prescription(doc_name=doc_name, symptoms=form_data['symptoms'],
                                        prescription=form_data['prescription'],
                                        patient_username=patient_username,
                                        patient_fullname=full_name)
            prescription.save()
            return redirect('home')
    else:
        form = CreatePrescription()
    context = {
        'form': form,
        'patient_list': patient_list
    }

    return render(req, 'users/create_prescription.html', context)


@login_required()
@user_passes_test(is_doc)
def list_of_prescriptions(req):
    prescriptions_list = Prescription.objects.all().filter(doc_name=req.user)
    context = {
        'prescriptions_list': prescriptions_list
    }
    return render(req, 'users/prescription.html', context)


@login_required()
@user_passes_test(is_patient)
def medical_history(req):
    prescriptions_list = Prescription.objects.all().filter(patient_username=req.user)
    context = {
        'prescriptions_list': prescriptions_list
    }
    return render(req, 'users/medical_history.html', context)
