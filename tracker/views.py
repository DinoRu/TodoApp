from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from .models import Task

class Login(LoginView):
	template_name = 'tracker/login.html'
	fields = "__all__"
	redirect_authenticated_user = True

	def get_success_url(self):
		return reverse_lazy('tracker:home')

class Register(FormView):
	template_name = 'tracker/register.html'
	form_class = UserCreationForm
	redirect_authenticated_user = True
	success_url = reverse_lazy('tracker:home')

	def form_valid(self, form):
		user = form.save()
		if user is not None:
			login(self.request, user)
		return super().form_valid(form)

	def get(self, *args, **kwargs):
		if self.request.user.is_authenticated:
			return redirect('tracker:home')
		return super().get(*args, **kwargs)



class TaskListView(LoginRequiredMixin, ListView):
	model = Task
	context_object_name = 'objects'
	template_name = 'tracker/home.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['objects'] = context['objects'].filter(user=self.request.user)
		context['count'] = context['objects'].filter(closed=False).count()

		search_input = self.request.GET.get('search-area') or ''
		if search_input:
			context['objects'] = context['objects'].filter(name__icontains=search_input)
		return context



class DetailTaskView(LoginRequiredMixin ,DeleteView):
	model = Task
	context_object_name = 'obj'
	template_name = 'tracker/detail.html'


class CreateTaskView(LoginRequiredMixin, CreateView):
	model = Task
	fields = ['name', 'description', 'due_date', 'schedule_date', 'closed']
	success_url = reverse_lazy('tracker:home')

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)



class DeleteTaskView(LoginRequiredMixin ,DeleteView):
	model = Task
	success_url = reverse_lazy('tracker:home')


class UpdateTaskView(LoginRequiredMixin ,UpdateView):
	model = Task
	fields = "__all__"
	template_name_suffix = "_update_form"
	success_url = reverse_lazy('tracker:home')

