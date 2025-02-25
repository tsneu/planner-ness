from django.urls import path
from .views import IndexView, TaskListView, form_plan_post, AnalytcView

urlpatterns = [
    path('', IndexView.as_view(), name='home_view'),
    path('task/<int:weekday>', TaskListView.as_view(), name='task_list'),
    path('note/edit', form_plan_post, name='form_plan_post'),
    path('chart', AnalytcView.as_view(), name='chart_view'),
]