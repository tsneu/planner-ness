from django.urls import path
from .views import IndexView, TaskListView

urlpatterns = [
    path('', IndexView.as_view(), name='home_view'),
    path('task/<int:weekday>', TaskListView.as_view(), name='task_list')
]