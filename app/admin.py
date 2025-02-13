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
    list_display = ['nome', 'sigla', 'descricao']


@admin.register(models.Anotacao)
class AnotacaoView(admin.ModelAdmin):
    list_display = ['ano', 'periodo', 'titulo', 'concluido']

    @admin.display()
    def periodo(self, obj):
        dtini = date.fromisocalendar(year=obj.ano, week=obj.semana, day=0)
        dtfim = date.fromisocalendar(year=obj.ano, week=obj.semana, day=6)
        return f'{dtini.strftime('%d/%m/%Y')} a {dtfim.strftime('%d/%m/%Y')}'


@admin.register(models.Local)
class LocalView(admin.ModelAdmin):
    list_display = ['nome', 'sigla']


@admin.register(models.Cronograma)
class CronogramaView(admin.ModelAdmin):
    list_display = ['data', 'titulo']


@admin.register(models.Atividade)
class AtividadeView(admin.ModelAdmin):
    list_display = ['cronograma', 'descricao', 'local', 'periodo', 'horario']
    