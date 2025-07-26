from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import PremierFormulaire, DeuxiemeFormulaire
from .models import Personne

def premier_formulaire(request):
    if request.method == 'POST':
        form = PremierFormulaire(request.POST)
        if form.is_valid():
            # Sauvegarder en session sans commit pour récupérer l'ID
            personne = form.save(commit=False)
            request.session['n_enregistrement'] = personne.n_enregistrement
            request.session['nom'] = personne.nom
            request.session['prenom'] = personne.prenom
            return redirect('deuxieme_formulaire')
    else:
        form = PremierFormulaire()
    return render(request, 'premier_formulaire.html', {'form': form})

def deuxieme_formulaire(request):
    if request.method == 'POST':
        form = DeuxiemeFormulaire(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        # Pré-remplir avec les données de la session
        initial_data = {
            'n_enregistrement': request.session.get('n_enregistrement', ''),
            'nom': request.session.get('nom', ''),
            'prenom': request.session.get('prenom', ''),
        }
        form = DeuxiemeFormulaire(initial=initial_data)
    return render(request, 'deuxieme_formulaire.html', {'form': form})

def success(request):
    return render(request, 'succes.html')


# views.py
# views.py
import plotly.express as px
from django.shortcuts import render

import plotly.express as px
from django.shortcuts import render

import plotly.express as px
from django.shortcuts import render
import pandas as pd

def view_view(request):
    # Données d'exemple
    df = pd.DataFrame({
        "label": ["A", "B", "C", "D", "E", "F"],
        "val":   [10, 23, 7, 15, 32, 18]
    })

    # Bar plot coloré
    fig = px.bar(
        df,
        x="label",
        y="val",
        color="label",  # chaque barre a sa couleur
        text="val",
        color_discrete_sequence=px.colors.qualitative.Dark24,  # palette qualitative
        title="Barres bien colorées",
        width = 800
    )

    fig.update_traces(textposition="outside")
    fig.update_layout(
        template="plotly_white",
        yaxis_title="Valeur",
        xaxis_title="",
        height=450
    )

    # Pas de fichier : on insère directement la <div> dans le template
    plot_div = fig.to_html(full_html=False, include_plotlyjs="cdn")
    return render(request, "plot.html", {"plot_div": plot_div})

import plotly.express as px
from django.shortcuts import render

def plot_view(request):
    df = {"label": ["A","B","C"], "val": [10, 20, 15]}
    fig = px.bar(df, x="label", y="val", color="label", text="val")
    fig.update_traces(textposition="outside")
    fig.update_layout(
        template="plotly_white",
        xaxis=dict(fixedrange=True),
        yaxis=dict(fixedrange=True),
        margin=dict(l=40, r=20, t=40, b=30),
        height=450,
        width = 800
    )

    plot_div = fig.to_html(
        full_html=False,
        include_plotlyjs="cdn",
        config={'displayModeBar': False}
    )
    return render(request, "plot.html", {"plot_div": plot_div})
