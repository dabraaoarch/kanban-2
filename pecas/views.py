from django.shortcuts import render,get_object_or_404,redirect,reverse
from .models import Peca, Aplicacao
from .forms import NovaPecaForm

def index(request):
    pecas = Peca.objects.all()
    context = {
        'pecas' : pecas
    }
    return render(request,'pecas/index.html', context)

def aplicacoes(request, peca_id):
    peca_aplicacao = get_object_or_404(Peca, pk=peca_id)
    if peca_aplicacao.aplicacao_set.filter(ativo=True).count() > 0:
        aplicacoes = peca_aplicacao.aplicacao_set.filter(ativo=True)
        context = {
            'peca_aplicacao' : peca_aplicacao,
            'aplicacoes' : aplicacoes 
        }
        return render(request, 'pecas/aplicacoes.html', context)
    else :
        return redirect(reverse('pecas:index'))

def nova_peca(request):
    if request.method == 'POST':
        form = NovaPecaForm(request.POST)
        if form.is_valid():
            peca = form.save(commit=False)
            peca.save()
            return redirect(reverse('pecas:index'))
    else:
        form = NovaPecaForm()
    return render(request, 'pecas/nova_peca.html', {'form':form})
