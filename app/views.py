from django.views.generic import ListView, TemplateView
from .models import Cronograma, Atividade, Anotacao
from datetime import date
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin
import random


def random_color_generator():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return f'rgb({r}, {g}, {b})'


@require_http_methods(['POST'])
def form_plan_post(request):
    tarefas = request.POST.getlist('tarefa')
    anotacoes = request.POST.getlist('anotacao')
    
    if tarefas:
        ids = [int(i) for i in tarefas]
        res = Atividade.objects.filter(id__in=ids).update(realizado=True)
        print('Atividades atualizadas: ', ids, res)

    if anotacoes:
        ids = [int(i) for i in anotacoes]
        res = Anotacao.objects.filter(id__in=ids).update(concluido=True)
        print('Anotações atualizadas: ', res)

    return HttpResponseRedirect('/')


class IndexView(LoginRequiredMixin, ListView):
    template_name = 'app/index.html'
    context_object_name = 'anotacao'

    def get_queryset(self):
        hoje = date.today()
        week = hoje.isocalendar()[1]
        dados = Anotacao.objects.filter(data__year=hoje.year, data__week=week)
        return dados
    

class TaskListView(LoginRequiredMixin, ListView):
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
            context['cronograma'] = cronograma.first()
            cronograma_id = cronograma.first().id
            context['atividades'] = Atividade.objects.filter(cronograma__id=cronograma_id)
        
        return context


    def concluded_task(self):
        try:
            id = self.request.POST.get('id')
            realizado = self.request.POST.get('realizado')
            object = Atividade.objects.get(pk=id)
            object.realizado = realizado
            object.save()
            msg = 'Atividade concluída com sucesso.'
            result = 'success'
        except Exception as e:
            msg = 'Falha ao concluir atividade.'
            print(e)
            result = 'fail'

        return JsonResponse({'result': result, 'data': msg})


class AnalytcView(LoginRequiredMixin, TemplateView):
    template_name = 'app/chart.html'
    MONTHS = ['','Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    WEEK_DAYS = ['', 'Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sab']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hoje = date.today()
        context['mes_atual'] = hoje
        obj_list = Atividade.objects.filter(cronograma__data__year=hoje.year)\
                .values('cronograma__data__month', 'realizado')\
                .annotate(qtd=Count('realizado')).order_by('cronograma__data__month')
        labels = list(obj_list.values_list('cronograma__data__month', flat=True))
        lb_meses = list(dict.fromkeys(labels))
        ds_meses = self.__qtd_mensal(obj_list, lb_meses)
        context['ds_ano_labels'] = [self.MONTHS[i] for i in lb_meses]
        context['ds_ano_realizado'] = ds_meses[0]
        context['ds_ano_nao_realizado'] = ds_meses[1]
         
        obj_dia = Atividade.objects.filter(cronograma__data__year=hoje.year)\
                .values('cronograma__data__week_day', 'realizado')\
                .annotate(qtd=Count('realizado')).order_by('cronograma__data__week_day')
        
        lb_dias = list(obj_dia.values_list('cronograma__data__week_day', flat=True))
        lb_dias = list(dict.fromkeys(lb_dias))
        ds_dias = self.__qtd_week_day(obj_dia)
        context['ds_dia_labels'] = [self.WEEK_DAYS[i] for i in lb_dias]
        context['ds_dia_realizado'] = ds_dias[0]
        context['ds_dia_nao_realizado'] = ds_dias[1]

        obj_categoria = Atividade.objects.filter(cronograma__data__year=hoje.year, cronograma__data__month=hoje.month)\
                .values('categoria__sigla', 'realizado')\
                .annotate(qtd=Count('realizado')).order_by('categoria__sigla')
        
        lb_categorias = list(obj_categoria.values_list('categoria__sigla', flat=True))
        lb_categorias = list(dict.fromkeys(lb_categorias))
        ds_categorias = self.__qtd_categorias(obj_categoria, lb_categorias)
        if None in lb_categorias:
            i = lb_categorias.index(None)
            lb_categorias[i] = 'Sem categoria'
        context['ds_categoria_labels'] = lb_categorias
        context['ds_categoria_realizado'] = ds_categorias[0]
        context['ds_categoria_nao_realizado'] = ds_categorias[1]

        obj_local = Atividade.objects.filter(cronograma__data__year=hoje.year, cronograma__data__month=hoje.month, realizado=True)\
                .values('local__sigla')\
                .annotate(qtd=Count('realizado'))
        lb_local = list(obj_local.values_list('local__sigla', flat=True))
        lb_local = list(dict.fromkeys(lb_local))
        ds_local = list(obj_local.values_list('qtd', flat=True))
        context['ds_local_labels'] = lb_local
        context['bg_colors'] = [random_color_generator() for i in range(len(lb_local))]
        context['ds_local'] = ds_local
        
        return context
    

    def __qtd_mensal(self, obj_list, lb_meses):
        tam = len(lb_meses)
        realizado = [0]*tam
        nrealizado = [0]*tam
        for item in obj_list:
            indice = lb_meses.index(item['cronograma__data__month'])
            if item['realizado']:
                realizado[indice] = item['qtd']
            else:
                nrealizado[indice] = item['qtd']

        return realizado, nrealizado


    def __qtd_week_day(self, obj_list):
        realizado = [0]*7
        nrealizado = [0]*7
        for item in obj_list:
            if item['realizado']:
                realizado[item['cronograma__data__week_day']-1] = item['qtd']
            else:
                nrealizado[item['cronograma__data__week_day']-1] = item['qtd']

        return realizado, nrealizado
    

    def __qtd_categorias(self, obj_list, categorias):
        tam = len(categorias)
        realizado = [0]*tam
        nrealizado = [0]*tam
        
        for item in obj_list:
            indice = categorias.index(item['categoria__sigla'])
            if item['realizado']:
                realizado[indice] = item['qtd']
            else:
                nrealizado[indice] = int(item['qtd'])
        nrealizado = [-i for i in nrealizado]
        return realizado, nrealizado
       