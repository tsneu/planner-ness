from django.db import models
from django.contrib.auth.models import User

class Departamento(models.Model):
    nome = models.CharField(max_length=30)
    sigla = models.CharField(max_length=10)
    descricao = models.CharField(max_length=255)

    def __str__(self):
        return self.nome


class Produto(models.Model):
    medida_choices = {
        'un': 'Unidade',
        'pc': 'Peça',
        'kg': 'Kilograma',
        'l': 'Litro',
        'cx': 'Caixa',
        'pt': 'Pacote',
        'kt': 'Kit',
        'ot': 'Outro',
    }
    nome = models.CharField(max_length=100)
    unidade_metrica = models.CharField(max_length=2, choices=medida_choices)
    departamento = models.ForeignKey(Departamento, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nome


class Categoria(models.Model):
    nome = models.CharField(max_length=30)
    sigla = models.CharField(max_length=10)
    descricao = models.CharField(max_length=255)

    def __str__(self):
        return self.nome


class Local(models.Model):
    nome = models.CharField(max_length=30)
    sigla = models.CharField(max_length=10)
    descricao = models.CharField(max_length=255)

    def __str__(self):
        return self.nome


class Cronograma(models.Model):
    data = models.DateField()
    titulo = models.CharField(max_length=100, null=True, blank=True)
    texto = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.data.strftime('%d/%m/%Y')
    

class Atividade(models.Model):
    AM = 'am'
    PM = 'pm'
    NT = 'nt'
    DY = 'dy'
    PERIODO_CHOICES = {
        AM: 'Manhã',
        PM: 'Tarde',
        NT: 'Noite',
        DY: 'Dia inteiro'
    }
    cronograma = models.ForeignKey(Cronograma, on_delete=models.DO_NOTHING)
    descricao = models.CharField(max_length=255)
    periodo = models.CharField(max_length=2, choices=PERIODO_CHOICES, null=True, blank=True)
    horario = models.TimeField(null=True, blank=True)
    realizado = models.BooleanField(default=False)
    local = models.ForeignKey(Local, on_delete=models.DO_NOTHING, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.descricao


class Compra(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.DO_NOTHING)
    atividade = models.ForeignKey(Atividade, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=255, null=True, blank=True)
    quantidade = models.DecimalField(max_digits=7, decimal_places=3, null=True, blank=True)
    preco = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.produto__nome


class Anotacao(models.Model):
    ano = models.SmallIntegerField()
    semana = models.SmallIntegerField()
    titulo = models.CharField(max_length=100)
    texto = models.CharField(max_length=255)
    concluido = models.BooleanField(default=False)

    class Meta:
        verbose_name = "anotação"
        verbose_name_plural = "anotações"
        ordering = ["-ano", "-semana"]

    def __str__(self):
        return self.titulo
    