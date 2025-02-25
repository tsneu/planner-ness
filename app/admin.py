from django.contrib import admin
from . import models
from datetime import date

admin.site.site_header = 'Plannerness - Rotina diária'
admin.site.site_title = 'Plannerness'

@admin.register(models.Departamento)
class DepartamentoView(admin.ModelAdmin):
    list_display = ['nome', 'sigla', 'descricao']


@admin.register(models.Produto)
class ProdutoView(admin.ModelAdmin):
    list_display = ['nome', 'unidade_metrica', 'departamento']


@admin.register(models.Categoria)
class CategoriaView(admin.ModelAdmin):
    list_display = ['nome', 'sigla', 'descricao', 'icone']


@admin.register(models.Anotacao)
class AnotacaoView(admin.ModelAdmin):
    list_display = ['periodo', 'titulo', 'concluido']    

    @admin.display()
    def periodo(self, obj):
        dt = obj.data
        week = dt.isocalendar()[1]
        dtini = date.fromisocalendar(year=dt.year, week=week, day=1)
        dtfim = date.fromisocalendar(year=dt.year, week=week, day=7)
        return f'{dtini.strftime('%d/%m/%Y')} a {dtfim.strftime('%d/%m/%Y')}'




@admin.register(models.Local)
class LocalView(admin.ModelAdmin):
    list_display = ['nome', 'sigla', 'icone']


@admin.register(models.Cronograma)
class CronogramaView(admin.ModelAdmin):
    list_display = ['data', 'dia', 'titulo']

    @admin.display()
    def dia(self, obj):
        dt = obj.data
        return f'{dt.strftime('%A')}'



@admin.register(models.Atividade)
class AtividadeView(admin.ModelAdmin):
    list_display = ['cronograma','dia', 'descricao', 'realizado', 'local', 'periodo', 'horario']
    list_filter = ['cronograma__data', 'local', 'categoria']
    actions = ['marcar_renovado', ]
    
    @admin.display()
    def dia(self, obj):
        dt = obj.cronograma.data
        return f'{dt.strftime('%A')}'

    @admin.action(description='Marcar como realizado')
    def marcar_renovado(self, request, queryset):
        res = queryset.update(realizado=True)
        self.message_user(request, 'Atualizado {} atividade(s).'.format(res))