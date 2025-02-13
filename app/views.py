from django.shortcuts import render
from django.views.generic import ListView
from .models import Cronograma, Atividade, Anotacao
from datetime import date

class IndexView(ListView):
    template_name = 'app/index.html'
    context_object_name = 'anotacao'

    def get_queryset(self):
        hoje = date.today()
        week = date.isocalendar(hoje)[1]
        dados = Anotacao.objects.filter(ano=hoje.year,semana=week)
        return dados
            

class TaskListView(ListView):
    template_name = 'app/task_day.html'
    context_object_name = 'cronograma'
    weekday = 0 # 1 = sunday, 7= saturday

    def get_queryset(self):
        self.weekday = self.kwargs["weekday"]
        hoje = date.today()
        week = date.isocalendar(hoje)[1]
        dados = Cronograma.objects.filter(data__year=hoje.year, data__week = week, data__week_day=self.weekday)
        return dados
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cronograma = context['cronograma']
        context['atividades'] = None
        if cronograma.exists():
            cronograma_id = cronograma.first().id
            context['atividades'] = Atividade.objects.filter(cronograma__id=cronograma_id)
        
        return context