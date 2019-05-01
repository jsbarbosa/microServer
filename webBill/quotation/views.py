from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import QuoteForm

from microbill import objects, correo

def index(request):
    form = QuoteForm()
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            dict_ = dict([(field, form.cleaned_data[field]) for field in form.FIELDS])
            muestra = form.cleaned_data['muestra']
            usuario = objects.Usuario(**dict_)
            servicio = objects.Servicio("013", cantidad = 1, interno = usuario.getInterno())
            cotizaciones = objects.crearCotizaciones(usuario, [servicio], muestra)
            objects.generarPDFs(cotizaciones)
            objects.guardarCotizaciones(cotizaciones)
            target, args = correo.correoTargetArgs(cotizaciones, "")
            target(*args)
            return redirect('exito')
    return render(request, 'index.html', context = {'form': form})

def exito(request):
    return render(request, 'exito.html')
