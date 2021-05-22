from django.db import models

class Gravitacional(models.Model):
    def __str__(self):
        return self.nome_gravitacional

    codigo = models.CharField(max_length=10)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    descricao = models.CharField(max_length=250)
    linha = models.CharField(max_length=10)
    posto = models.CharField(max_length=10)
    galpao = models.CharField(max_length=10)

    def get_pecas_gravitacional(self):
        return self.aplicacao_set.filter(ativo=True).count()
    
