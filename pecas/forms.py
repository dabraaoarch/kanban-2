from django import forms
from .models import *

class NovoAbastecimentoForm(forms.ModelForm):
    class Meta:
        model = Abastecimento
        fields = ['codigo']
        labels = {
            'codigo' : 'Código pedido'
        }
        
    def lines_count(self):
        if len(self.fields) % 2 != 0:
            return len(self.fields) + 1
        return len(self.fields)


class NovaPecaForm(forms.ModelForm):
    class Meta:
        model = Peca
        fields = ['codigo_peca', 'nome_peca']
        labels = {
            'codigo_peca': 'Código peça',
            'nome_peca': 'Nome peça'
        }
    def lines_count(self):
        if len(self.fields) % 2 != 0:
            return len(self.fields) + 1
        return len(self.fields)

        

class NovoGravitacionalForm(forms.ModelForm):
    class Meta:
        model = Gravitacional
        fields = [
            'codigo',
            'descricao',
            'posto',
            'linha',
            'galpao'
        ]
        labels = {
            'codigo': 'Código',
            'descricao' : 'Descrição',
            'galpao' : 'Galpão'
        }
        
    def lines_count(self):
        if len(self.fields) % 2 != 0:
            return len(self.fields) + 1
        return len(self.fields)

class NovaAplicacaoForm(forms.ModelForm):
    class Meta:
        model = Aplicacao
        fields = [
            'peca_aplicacao',
            'embalagem'
        ]
        labels = {
            'peca_aplicacao' : "Peça"
        }
        
    def lines_count(self):
        if len(self.fields) % 2 != 0:
            return len(self.fields) +1
        return len(self.fields)

