from django.db import models
from gravitacionais.models import Gravitacional

class Peca(models.Model):
    def __str__(self):
        return self.nome_peca

    nome_peca = models.CharField(max_length=100)
    codigo_peca = models.CharField(max_length=20, unique=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def get_aplicacoes(self):
        return self.aplicacao_set.filter(ativo=True).count()

class Aplicacao(models.Model):
    def __str__(self):
        return self.peca_aplicacao.nome_peca
    peca_aplicacao = models.ForeignKey(Peca, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=100)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)
    embalagem = models.CharField(max_length=10, default='')
    gravitacional_aplicacao = models.ForeignKey(
        Gravitacional,
        on_delete=models.CASCADE
    )

