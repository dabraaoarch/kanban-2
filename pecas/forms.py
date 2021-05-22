from django import forms
from .models import Peca, Aplicacao

class NovaPecaForm(forms.ModelForm):
    class Meta:
        model = Peca
        fields = ['codigo_peca', 'nome_peca']
        labels = {
            'codigo_peca': 'Código peça',
            'nome_peca': 'Nome peça'
        }
        
