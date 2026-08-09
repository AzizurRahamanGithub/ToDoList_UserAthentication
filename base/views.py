from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task

# Create your views here.


class UserLogin(LoginView):
    template_name= 'base/login.html'
    redirect_authenticated_user= True

    def get_success_url(self):
        return reverse_lazy('tasks')

class UserRegister(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(UserRegister, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(UserRegister, self).get(*args, **kwargs)  # Call the superclass method for unauthenticated users




class TaskList(ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        tasks = context['tasks'].filter(user=self.request.user)
        context['tasks'] = tasks
        
        context['count'] = tasks.filter(complete=False).count()

        search_input = self.request.GET.get("search-area", '').strip()
        
        if search_input:
            context['tasks'] = tasks.filter(title__startswith=search_input)
        
        context['search_input'] = search_input
        
        return context



class TaskDetail(DetailView):
    model= Task
    context_object_name= 'task'    


class TaskCreate(CreateView):
    model= Task
    fields= ['title', 'description', 'complete']
    success_url= reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user= self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(UpdateView):
    model= Task
    fields= ['title', 'description', 'complete']
    success_url= reverse_lazy('tasks')

class TaskDelete(DeleteView):
    model= Task
    context_object_name= 'task_dlt'    
    success_url= reverse_lazy('tasks')
