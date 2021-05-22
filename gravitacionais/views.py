from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect, reverse
from .models import Gravitacional
from .forms import NovoGravitacionalForm, NovaAplicacaoForm
from pecas.models import Aplicacao

def index(request):
    gravitacionais = Gravitacional.objects.all()
    context = {
        'gravitacionais' : gravitacionais
    }
    return render(request, 'gravitacionais/index.html', context)

def novo_gravitacional(request):
    if request.method == 'POST':
        form = NovoGravitacionalForm(request.POST)
        if form.is_valid():
            gravitacional = form.save(commit=False)
            gravitacional.save()
            return redirect(reverse('gravitacionais:index'))
    else:
        form = NovoGravitacionalForm()
    return render(
        request,
        'gravitacionais/novo_gravitacional.html',
        {'form':form}
    )

def gerir_gravitacional(request, gravitacional_id):
    gravitacional = get_object_or_404(
        Gravitacional,
        pk=gravitacional_id
    )
    if request.method == 'POST':
        form = NovaAplicacaoForm(request.POST)
        if form.is_valid():
            aplicacao = form.save(commit=False)
            aplicacao.gravitacional_aplicacao = gravitacional
            aplicacao.save()
            
    form = NovaAplicacaoForm()        
    aplicacoes = gravitacional.aplicacao_set.filter(ativo=True)
    context = {
        'gravitacional' : gravitacional,
        'aplicacoes': aplicacoes,
        'form' : form
    }
    return render(
        request,
        'gravitacionais/gerir_gravitacional.html',
        context
    )

def remover_aplicacao(request, aplicacao_id):
    aplicacao = get_object_or_404(Aplicacao, pk=aplicacao_id)
    gravitacional = aplicacao.gravitacional_aplicacao
    aplicacao.ativo = False
    aplicacao.save()
    return redirect(
        reverse(
            'gravitacionais:gerir_gravitacional',
            kwargs = {
                'gravitacional_id' : gravitacional.id
            }
        )                
    )

def imprimir_etiquetas(request, gravitacional_id):
      gravitacional = get_object_or_404(
          Gravitacional,
          pk=gravitacional_id
      )
      aplicacoes = gravitacional.aplicacao_set.filter(ativo=True)
      context = {
          'gravitacional' : gravitacional,
          'aplicacoes' : aplicacoes
      }
      return render(request, 'gravitacionais/etiquetas.html', context)
  
