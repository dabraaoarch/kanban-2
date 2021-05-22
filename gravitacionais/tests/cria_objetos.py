from pecas.models import Peca, Aplicacao
from ..models import Gravitacional

def cria_pecas(
        codigo_peca='123',
        nome_peca='peca'
):
    '''
    Create an item object to run the tests
    '''
    return Peca.objects.create(
        codigo_peca=codigo_peca,
        nome_peca=nome_peca
    )

def cria_aplicacao(
        peca=None,
        gravitacional=None,
        embalagem = '529',
        descricao = 'aplicacao de teste'
):
    '''
    Create an application object to run the tests
    '''
    if peca == None:
        peca = cria_pecas()
    
    if gravitacional == None:
        gravitacional = cria_gravitacional()
            
    return Aplicacao.objects.create(
        peca_aplicacao=peca,
        embalagem=embalagem,
        descricao=descricao,
        gravitacional_aplicacao = gravitacional
    )

def cria_gravitacional(
        codigo = '123',
        descricao = 'gravitacional de ilha',
        posto = '10',
        linha = '3',
        galpao = 'A'
):
    '''
    Create a gravitacional object for run the tests
    '''
    return Gravitacional.objects.create(
        codigo = codigo,
        descricao=descricao,
        posto=posto,
        linha=linha,
        galpao=galpao,
    )
