from django.db import models

class Peca(models.Model):
    def __str__(self):
        return self.nome_peca

    nome_peca = models.CharField(max_length=100)
    codigo_peca = models.CharField(max_length=20, unique=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

class Gravitacional(models.Model):
    def __str__(self):
        return self.nome_gravitacional

    codigo = models.CharField(max_length=10)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    descricao = models.CharField(max_length=250)
    linha = models.CharField(max_length=10)
    posto = models.CharField(max_length=10)
    galpao = models.CharField(max_length=10)

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

    
class Abastecimento(models.Model):
    def __str__(self):
        return self.codigo

    codigo = models.CharField(max_length=100)
    aplicacao = models.ForeignKey(Aplicacao, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    situacao = models.CharField(max_length=10, default='requisitado')

    def valida_codigo(self):
        '''
        checks if the code have the right pattern 
        '''
        divisoes_codigo_pedido = 4
        if self.codigo.count('*') == divisoes_codigo_pedido \
           and len(self.codigo) > divisoes_codigo_pedido:
            return True
        return False
    
    def get_codigo_gravitacional(self):
        '''
        for the right pattern returns the gravitacional code
        '''
        if self.valida_codigo():
            return self.codigo.split('*')[1]

    def get_codigo_peca(self):
        '''
        for the right pattern return the peca code
        '''
        if self.valida_codigo():
            return self.codigo.split('*')[2]

    def get_codigo_aplicacao(self):
        '''
        for the right pattern return the peca code
        '''
        if self.valida_codigo():
            return self.codigo.split('*')[3]
