from typing import Any, Optional, Union
from django.db import models
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.http.response import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect,render
from django.views.generic import FormView,CreateView,TemplateView,DeleteView,View,UpdateView,DetailView,ListView
from .forms import *
from .models import *
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from typing import Any, Dict
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query import QuerySet
from django.urls import reverse

def init_app(request):
    if Group.objects.all().count() < 2:
        employee_group = Group(name='employee')
        employer_group = Group(name='employer')
        employee_group.save()
        employer_group.save()
    return redirect('home')


class HomeView(TemplateView):

    template_name = 'home.html'
    context_object_name = 'user_role'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if self.request.user.groups.first() != None:
            if self.request.user.groups.first().name == 'employer':
                context['user_role'] = 'employer'
                user_role_model = get_object_or_404(Employer,user=self.request.user)
                context['user_role_model'] = user_role_model
                return context
            if self.request.user.groups.first().name == 'employee':
                context['user_role'] = 'employee'
                user_role_model = get_object_or_404(Employee,user=self.request.user)
                context['user_role_model'] = user_role_model
                print
                return context
        return context


class ChoiceRoleView(TemplateView):

    template_name = 'choice_role.html'


class RegistrationEmployeeView(CreateView):

    template_name = 'registration_employee.html'
    success_url = 'login'  
    form_class = RegistrationEmployeeForm

    def form_valid(self, form: RegistrationEmployeeForm) -> HttpResponse:
        user = form.save()
        group = Group.objects.get(name='employee')
        user.groups.add(group)
        new_employee = Employee(user=user)
        new_employee.save()
        messages.info(self.request,f'Zarejestrowano użytkownika {user.username}')
        return super().form_valid(form)

class RegistrationEmployerView(CreateView):

    template_name = 'registration_employee.html'
    success_url = 'login'  
    form_class = RegistrationEmployeeForm

    def form_valid(self, form: RegistrationEmployerForm) -> HttpResponse:
        user = form.save()
        group = Group.objects.get(name='employer')
        user.groups.add(group)
        new_employee = Employer(user=user)
        new_employee.save()
        messages.info(self.request,f'Zarejestrowano użytkownika {user.username}')
        return super().form_valid(form)
    

class LoginView(FormView):

    template_name = 'login.html'
    form_class = LoginForm

    def form_valid(self, form: LoginForm) -> HttpResponse:
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request,username=username,password=password)
        if user is not None:
            login(self.request,user=user)
            return redirect('home')
        else:
            return redirect('login')
        

class LogoutView(View):

    def get(self,*args,**kwargs) -> HttpResponse:
        logout(self.request)
        return redirect('home')
        

class EmployeeProfile(DetailView):

    template_name = 'employee_profile.html'
    model = Employee
    context_object_name = 'employee'
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user = User.objects.get(id=self.kwargs['pk'])
        context['employee'] = Employee.objects.get(user=user.id)
        return context
    

class EmployerProfile(DetailView):

    template_name = 'employer_profile.html'
    model = Employer
    context_object_name = 'employer'
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user = User.objects.get(id=self.kwargs['pk'])
        context['employer'] = Employer.objects.get(user=user.id)
        return context
    

def VerifyUserProfile(instance: Union[EmployeeProfile,EmployerProfile], model: models.Model) -> bool:
    user = instance.request.user
    try:
        profile_user = model.objects.get(id=instance.kwargs['pk'])
        if user == profile_user.user:
            return True
        return False
    except ObjectDoesNotExist:
        return False



class EmployeeProfile(LoginRequiredMixin,UserPassesTestMixin,DetailView):

    template_name = 'employee_profile.html'
    model = Employee
    login_url = 'login'

    def test_func(self) -> bool | None:
        result = VerifyUserProfile(self,Employee)
        return result
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        employee_user = Employee.objects.get(pk=self.kwargs['pk'])
        jobs = EmployeeJob.objects.filter(job_user=employee_user)
        languages = EmployeeLanguage.objects.filter(language_user=employee_user)
        context['employee_user'],context['jobs'],context['languages'] = employee_user,jobs,languages
        return context


    

class EmployerProfile(LoginRequiredMixin,UserPassesTestMixin,DetailView):

    template_name = 'employer_profile.html'
    model = Employer
    login_url = 'login'
        
    def test_func(self) -> bool :
        result = VerifyUserProfile(self,Employer)
        return result

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['employer'] = Employer.objects.get(id=self.kwargs['pk'])
        return context



class EditBaseInformationEmployeeView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):

    template_name = 'update_information_employee.html'
    login_url = 'login'
    model = Employee
    form_class = UpdateBaseInformationEmployeeForm
    pk_url_kwarg = 'pk'

    def test_func(self) -> bool :
        result = VerifyUserProfile(self,Employee)
        return result
    
    def get_success_url(self) -> str:
        pk = self.kwargs['pk']
        url = reverse('employee_profile', kwargs={'pk': pk})
        return url
    

class AddLanguageView(LoginRequiredMixin,UserPassesTestMixin,CreateView):

    login_url = 'login'
    model = EmployeeLanguage
    form_class =CreateEmployeeLanguageForm
    template_name = 'add_language.html'

    def test_func(self) -> bool :
        result = VerifyUserProfile(self,Employee)
        return result

    def get_success_url(self) -> str:
        pk = self.kwargs['pk']
        url = reverse('employee_profile', kwargs={'pk': pk})
        return url

    def form_valid(self, form: CreateEmployeeLanguageForm) -> HttpResponse:
        form = CreateEmployeeLanguageForm(self.request.POST)
        user = Employee.objects.get(user=self.request.user)
        form.instance.language_user = user
        return super().form_valid(form)
        


class EditLanguageView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):

    template_name = 'update_language.html'
    login_url = 'login'
    model = EmployeeLanguage
    form_class = UpdateLanguageEmployeeForm
    pk_url_kwarg = 'pk_lang'

    def test_func(self) -> bool :
        result = VerifyUserProfile(self,Employee)
        return result
    
    def get_success_url(self) -> str:
        pk = self.kwargs['pk']
        url = reverse('employee_profile', kwargs={'pk': pk})
        return url
    
    def get_object(self, queryset: QuerySet[Any] | None = ...) -> EmployeeLanguage:
        language = EmployeeLanguage.objects.get(id=self.kwargs['pk_lang'])
        return language
    

class DeleteLanguageView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):

    login_url = 'login'
    model = EmployeeLanguage
    context_object_name = 'language'
    pk_url_kwarg = 'pk_lang'

    def test_func(self) -> bool :
        result = VerifyUserProfile(self,Employee)
        return result
    
    def get_success_url(self) -> str:
        pk = self.kwargs['pk']
        url = reverse('employee_profile', kwargs={'pk': pk})
        return url
    
    def get_object(self, queryset: QuerySet[Any] | None = ...) -> EmployeeLanguage:
        language = EmployeeLanguage.objects.get(id=self.kwargs['pk_lang'])
        return language

    def delete(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


    # moze lepiej zmienic na zwykly wyidok, bez potwierdzen







class AddJobView(LoginRequiredMixin,UserPassesTestMixin,CreateView):

    login_url = 'login'
    model = EmployeeJob
    form_class = CreateEmployeeJobForm
    template_name = 'add_job_history.html'

    def test_func(self) -> bool :
        result = VerifyUserProfile(self,Employee)
        return result

    def get_success_url(self) -> str:
        pk = self.kwargs['pk']
        url = reverse('employee_profile', kwargs={'pk': pk})
        return url
    
    def form_valid(self, form: CreateEmployeeJobForm) -> HttpResponse:
        form = CreateEmployeeJobForm(self.request.POST)
        user = Employee.objects.get(user=self.request.user)
        form.instance.job_user = user
        return super().form_valid(form)



class JobEditView():
    pass

class JobDeleteView():
    pass









class EditBaseInformationEmployerView(LoginRequiredMixin,UserPassesTestMixin,TemplateView):

    template_name = ''
    login_url = 'login'

    def test_func(self) -> bool :
        result = VerifyUserProfile(self,Employer)
        return result
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        return super().get_context_data(**kwargs)



