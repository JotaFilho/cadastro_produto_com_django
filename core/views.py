from email import message
from multiprocessing import context
from django import forms
from django.shortcuts import render
from .forms import ContatoForm, ProdutoModelForm
from django.contrib import messages
from .models import Produto
from django.shortcuts import redirect

def index(request):
    context = {
        'produtos': Produto.objects.all()
    }
    return render(request, 'index.html', context)

def contact(request):
    form = ContatoForm(request.POST or None)
    
    if str(request.method) == 'POST':
        if form.is_valid():
            form.send_mail()
            
            messages.success(request, 'E-mail enviado com sucesso')
            form = ContatoForm()
        else:
            messages.error(request, 'Erro ao enviar e-mail')
    context = {
        'form': form
    }
    return render(request, 'contact.html', context)

def product(request):
    if str(request.user) != "AnonymousUser":
        if str(request.method) == 'POST':
            form = ProdutoModelForm(request.POST, request.FILES)
            if form.is_valid():
            
                form.save()
            
                messages.success(request, 'Produto Salvo com sucesso.')
                form = ProdutoModelForm()
            else:
                messages.error(request, 'Produto não foi salvo')
        else:
            form = ProdutoModelForm()
        context = {
            'form': form
        }
        return render(request, 'product.html', context)
    else:
        return redirect('index')