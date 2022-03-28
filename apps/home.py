from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
from app import app
import pandas as pd
import functions as fc

layout = dbc.Container([
    dbc.Row([
        html.H1('Élection Présidentielle 2022', className='text-center bg-info text-white')
    ]),
    dbc.Row([
        dcc.Markdown("""
                ### Application Description:
                In this dashboard, we present a daily follow up of the French Presidentiel Election 2022.

                It is based on the daily published tweets. To update the tweets extraction please push the refresh button.
        """)
    ]),

    dbc.Row([
        dcc.Markdown("""
                ### According to the French Senat, these are the official candidates for the presidential election:

                * Emmanuel macron
                * Eric Zemmour
                * Marine Le Pen
                * Jean-Luc Mélenchon
                * Nathalie Arthaud
                * Fabien Roussel
                * Jean Lassalle
                * Anne Hidalgo
                * Yannick Jadot
                * Valérie Pécresse
                * Philippe Poutou
                * Nicolas Dupont-Aignan
        """)
    ])
])
