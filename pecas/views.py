from django.shortcuts import render, get_list_or_404, \
    get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import *
from .forms import NovoGravitacionalForm, NovaAplicacaoForm, \
    NovaPecaForm, NovoAbastecimentoForm
from django.views.generic import CreateView, ListView
from django.utils.decorators import method_decorator
from collections import defaultdict

@method_decorator(login_required, name='dispatch')
class NovaPecaView(CreateView):
    model = Peca
    form_class = NovaPecaForm
    success_url = reverse_lazy('pecas:nova_peca')
    template_name = 'pecas/nova_peca.html'

    def get_context_data(self, **kwargs):
        kwargs['pecas'] = Peca.objects.order_by(
            '-data_cadastro'
        ).annotate(
            count_aplicacao=Count('aplicacao')
        )[:10]
        return super().get_context_data(**kwargs)

@method_decorator(login_required, name='dispatch')
class PecasListView(ListView):
    model = Peca
    context_object_name = 'pecas'
    template_name = 'pecas/index.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = Peca.objects.order_by(
            '-data_cadastro'
        ).annotate(
            count_aplicacao=Count('aplicacao')
        )
        return queryset

@method_decorator(login_required, name='dispatch')
class PedidosListView(CreateView):
    model = Abastecimento
    context_object_name = 'pedidos'
    form_class = NovoAbastecimentoForm
    template_name = 'abastecimentos/pendentes.html'
    paginate_by = 10
    tipo_pedidos = 'pendentes'

    def get(self, request, *args, **kwargs):
        self.tipo_pedidos = kwargs['tipo_pedido']
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.tipo_pedidos = kwargs['tipo_pedido']
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        criterios = defaultdict(lambda: 'requisitado')
        criterios = {
            'pendentes' : 'requisitado',
            'transporte' : 'transporte',
            'concluidos' : 'concluido'
        }
        kwargs['pedidos'] = Abastecimento.objects.filter(
            situacao = criterios[self.tipo_pedidos]
        ).order_by(
            '-data'
        )
        kwargs['tipo_pedido'] = self.tipo_pedidos
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        codigo_pedido = form.cleaned_data['codigo']
        if self.tipo_pedidos == 'pendentes':
            abastecimento = Abastecimento(
                codigo = codigo_pedido
            )
            aplicacao = get_object_or_404(
                Aplicacao,
                pk = abastecimento.get_codigo_aplicacao()
            )
            abastecimento.aplicacao = aplicacao
        else:
            if self.tipo_pedidos == 'transporte':
                abastecimento = get_list_or_404(
                    Abastecimento,
                    codigo = codigo_pedido,
                    situacao = 'requisitado'
                )[0]
                abastecimento.situacao = 'transporte'

            if self.tipo_pedidos == 'concluidos':
                abastecimento = get_list_or_404(
                    Abastecimento,
                    codigo = codigo_pedido,
                    situacao = 'transporte'
                )[0]
                abastecimento.situacao = 'concluido'

        abastecimento.save()
        return redirect(
            reverse(
                'pecas:pedidos',
                kwargs = {
                    'tipo_pedido' : self.tipo_pedidos
                }
            )
        )

@method_decorator(login_required, name='dispatch')
class GravitacionalListView(ListView):
    model = Gravitacional
    paginate_by = 10
    template_name = 'gravitacionais/gravitacionais.html'
    context_object_name = 'gravitacionais'

    def get_queryset(self):
        queryset = Gravitacional.objects.all().annotate(
            count_aplicacao=Count('aplicacao')
        ).order_by('-data_cadastro')
        return queryset

@method_decorator(login_required, name='dispatch')
class AplicacaoListView(ListView):
    model = Aplicacao
    paginate_by = 10
    template_name = 'pecas/aplicacoes.html'
    context_object_name = 'aplicacoes'

    def get(self, request, *args, **kwargs):
        self.peca_id = kwargs['peca_id']
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['peca_aplicacao'] = get_object_or_404(
            Peca,
            pk = self.peca_id
        )
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        queryset = Aplicacao.objects.filter(
            peca_aplicacao_id = self.peca_id
        ).order_by('-data_cadastro')
        return queryset

@method_decorator(login_required, name='dispatch')
class NovoGravitacionalView(CreateView):
    form_class = NovoGravitacionalForm
    model = Gravitacional
    template_name = 'gravitacionais/novo_gravitacional.html'
    success_url = reverse_lazy('pecas:gravitacionais')


@method_decorator(login_required, name='dispatch')
class GerirGravitacionalView(CreateView):
    form_class = NovaAplicacaoForm
    model = Aplicacao
    template_name = 'gravitacionais/gerir_gravitacional.html'

    def get_context_data(self, **kwargs):
        self.gravitacional = get_object_or_404(
            Gravitacional,
            pk = self.gravitacional_id
        )
        kwargs['aplicacoes'] = Aplicacao.objects.filter(
            gravitacional_aplicacao = self.gravitacional
        )
        kwargs['gravitacional'] = self.gravitacional
        return super().get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        self.gravitacional_id = kwargs['gravitacional_id']
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.gravitacional_id = kwargs['gravitacional_id']
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        gravitacional = get_object_or_404(
            Gravitacional,
            pk = self.gravitacional_id
        )

        aplicacao = form.save(commit=False)
        aplicacao.gravitacional_aplicacao = gravitacional
        aplicacao.save()
        return redirect(
            reverse(
                'pecas:gerir_gravitacional',
                kwargs = {
                    'gravitacional_id' : self.gravitacional_id
                }
            )
        )

@method_decorator(login_required, name='dispatch')
class EtiquetasListView(ListView):
    model = Aplicacao
    context_object_name = "aplicacoes"
    template_name = "gravitacionais/etiquetas.html"

    def get(self, request, *args, **kwargs):
        self.gravitacional_id = kwargs['gravitacional_id']
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['gravitacional'] = get_object_or_404(
            Gravitacional,
            pk = self.gravitacional_id
        )
        return super().get_context_data(**kwargs)

    def get_queryset(self, **kwargs):
        gravitacional = get_object_or_404(
            Gravitacional,
            pk = self.gravitacional_id
        )
        queryset = Aplicacao.objects.filter(
            gravitacional_aplicacao = gravitacional,
            ativo = True
        )
        return queryset

@login_required
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

@login_required
def remover_gravitacional(request, gravitacional_id):
    gravitacional = get_object_or_404(
        Gravitacional,
        pk = gravitacional_id
    )
    gravitacional.delete()
    return redirect(reverse('pecas:gravitacionais'))

@login_required
def remover_peca(request, peca_id):
    peca = get_object_or_404(Peca, pk=peca_id)
    peca.delete()
    return redirect(reverse('pecas:index'))

@login_required
def apagar_abastecimento(request, abastecimento_id):
    tipo_pedido = {
        'concluido' : 'concluidos',
        'requisitado' : 'pendentes',
        'transporte' : 'transporte'
    }
    abastecimento = get_object_or_404(
        Abastecimento,
        pk=abastecimento_id
    )
    pagina = tipo_pedido[abastecimento.situacao]
    abastecimento.delete()
    return redirect(
        reverse(
            'pecas:pedidos',
            kwargs={
                'tipo_pedido' : pagina
            }
        )
    )

