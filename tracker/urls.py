from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views


app_name = 'tracker'
urlpatterns = [
	path('login/', views.Login.as_view(), name='login'),
	path('logout/', LogoutView.as_view(next_page='tracker:login'), name='logout'),
	path('register/', views.Register.as_view(), name='register'),
	path('', views.TaskListView.as_view(), name='home'),
	path('<int:pk>/', views.DetailTaskView.as_view(), name='detail'),
	path('tracker/create_task/', views.CreateTaskView.as_view(), name="create"),
	path('tracker/<int:pk>/delete/', views.DeleteTaskView.as_view(), name='delete'),
	path('tracker/<int:pk>/update/', views.UpdateTaskView.as_view(), name='update'),
]