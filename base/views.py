from dataclasses import field
import imp
from pyexpat import model
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView #za ispisivanje detalja kolone
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy #redirecta usera na drugio dio app-a

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task

class CustomLoginView (LoginView):
    template_name = 'base/login.html'
    fields = '__all__' #list outa sve colone
    redirect_authenticated_user = True
    #ako je user authenticated ne bi treabli biti na ovoj stranici
    def get_success_url(self):
        return reverse_lazy('tasks')

class RegisterPage (FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks') 

    def form_valid (self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, *kwargs)

class TaskList(LoginRequiredMixin, ListView):  #class base view dodati ga u urlpattern
    model = Task
    context_object_name = 'tasks'
     #da mozes stavljati drugacije ime u template

    def get_context_data (self, **kwargs): #**kwargs allows you to handle named arguments that you have not defined in advance
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)   
        context['count'] = context['tasks'].filter(complete=False).count() #koliko ima nezavršenih taskova
        #ovako mozes passati context datu # pokazat ce taskove od loganog usera

        search_input = self.request.GET.get('search-area') or ''    #prazno polje je default
        if search_input:
            context['tasks'] = context['tasks'].filter( #searchamo po title od taska
                title__startswith=search_input)

        context['search_input'] = search_input
        
        return context

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'
    #da mozes staviti drugacije ime template-a

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete'] #list outa iteme koje mi zelimo
    success_url = reverse_lazy('tasks') 
    #kad kreiras item posalji usera na listu taskova

    def form_valid(self, form): #funkcija u CreateView gdje user moze dodati samo sebi task
        form.instance.user = self.request.user #make sure its the loged in user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete'] 
    success_url = reverse_lazy('tasks')

class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')