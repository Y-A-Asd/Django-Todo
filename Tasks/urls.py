from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = "tasks"
urlpatterns = [
    path('', views.TaskListView.as_view(), name="tasks"),
    path('task/<int:pk>/', views.TaskDetailView.as_view(), name="task"),
    path('create_task/', views.TaskCreateView.as_view(), name="task_create"),
    path('update_task/<int:pk>/', views.TaskUpdateView.as_view(), name="task_update"),
    path('delete_task/<int:pk>/', views.TaskDeleteView.as_view(), name="task_delete"),

    path('login', views.LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(next_page='tasks:login'), name="logout"),
    path('register', views.RegisterView.as_view(), name="register"),
]
