from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView,FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


# Create your views here.

class TaskListView(LoginRequiredMixin, ListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        search = self.request.GET.get('search') or ''
        if search :
            context['tasks'] = context['tasks'].filter(title__icontains=search)
        return context

    model = Task
    context_object_name = "tasks"


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "Tasks/task_detail.html"
    context_object_name = "task"


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasks:tasks')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreateView, self).form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('tasks:tasks')


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = "task"
    success_url = reverse_lazy('tasks:tasks')


class LoginView(LoginView):
    template_name = "Tasks/login.html"
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks:tasks')

class RegisterView(FormView):
    template_name = 'Tasks/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('tasks:tasks')
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request,user)
        return super(RegisterView,self).form_valid(form)

    redirect_authenticated_user = True
    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks:tasks')
        else:super(RegisterView,self).get(*args,**kwargs)

