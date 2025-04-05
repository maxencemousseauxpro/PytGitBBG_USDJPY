import dash
from dash import dcc, html
from dash.dash_table import DataTable
import plotly.graph_objs as go
import sqlite3
import pandas as pd
from datetime import datetime

# Créer l'application Dash
app = dash.Dash(__name__)

# Fonction pour récupérer les données depuis la base de données SQLite
def get_data():
    conn = sqlite3.connect('usdjpy_prices.db')
    query = "SELECT * FROM prices ORDER BY timestamp DESC LIMIT 100"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Fonction pour calculer la volatilité quotidienne
def calculate_daily_volatility(df):
    return df['price'].std()

# Fonction pour calculer l'évolution du prix
def calculate_price_evolution(df):
    open_price = df['price'].iloc[-1]  # Dernier prix de la journée (ouverture)
    close_price = df['price'].iloc[0]  # Premier prix de la journée (fermeture)
    return close_price - open_price

# Mise en page de l'application avec des styles personnalisés
app.layout = html.Div(
    children=[
        # Titre du dashboard
        html.H1("USD/JPY Price Tracker", style={'textAlign': 'center', 'color': '#0D47A1', 'fontSize': '50px'}),
        
        # Afficher le prix actuel de l'USD/JPY
        html.Div(id='live-update-price', style={'textAlign': 'center', 'fontSize': '24px', 'color': '#1E88E5'}),
        
        # Graphique de l'USD/JPY au fil du temps
        dcc.Graph(id='live-update-graph'),
        
        # Mise à jour toutes les 5 minutes
        dcc.Interval(
            id='interval-component',
            interval=5*60*1000,  # Mise à jour toutes les 5 minutes
            n_intervals=0
        ),
        
        # Section pour le rapport quotidien à 20h
        html.Div(id='live-update-20h-report', style={'textAlign': 'center', 'fontSize': '18px', 'color': '#424242', 'marginTop': '20px'}),
    ],
    style={'backgroundColor': '#f0f4f8', 'padding': '20px'}  # Couleur de fond pour la page
)

# Callback pour mettre à jour le prix actuel de l'USD/JPY
@app.callback(
    dash.dependencies.Output('live-update-price', 'children'),
    [dash.dependencies.Input('interval-component', 'n_intervals')]
)
def update_price(n):
    with open('price.txt', 'r') as f:
        price = f.read().strip()
    return f"Current USD/JPY Price: {price}"

# Callback pour mettre à jour le graphique
@app.callback(
    dash.dependencies.Output('live-update-graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    df = get_data()
    if len(df) > 0:
        return {
            'data': [go.Scatter(x=df['timestamp'], y=df['price'], mode='lines+markers')],
            'layout': go.Layout(
                title='USD/JPY Price over Time',
                xaxis=dict(title='Time', showgrid=False),
                yaxis=dict(title='Price', showgrid=True),
                hovermode='closest',
                plot_bgcolor='#ffffff',
                paper_bgcolor='#f0f4f8',
                font=dict(family='Arial, sans-serif', size=14)
            )
        }

# Callback pour mettre à jour le rapport quotidien à 20h
@app.callback(
    dash.dependencies.Output('live-update-20h-report', 'children'),
    [dash.dependencies.Input('interval-component', 'n_intervals')]
)
def update_20h_report(n):
    current_time = datetime.now()

    # Vérifier si l'heure actuelle est 20h
    if current_time.hour == 20:
        df = get_data()
        if len(df) > 0:
            # Calculer les métriques quotidiennes
            daily_volatility = calculate_daily_volatility(df)
            price_evolution = calculate_price_evolution(df)

            # Créer le tableau du rapport
            report_table = [
                {'Metric': 'Daily Volatility', 'Value': f'{daily_volatility:.4f}'},
                {'Metric': 'Price Evolution', 'Value': f'{price_evolution:.2f}'}
            ]

            return DataTable(
                data=report_table,
                columns=[
                    {'name': 'Metric', 'id': 'Metric'},
                    {'name': 'Value', 'id': 'Value'}
                ],
                style_table={'width': '50%', 'margin': 'auto'},
                style_cell={'textAlign': 'center', 'padding': '10px', 'border': '1px solid #ddd'},
                style_header={'backgroundColor': '#f0f4f8', 'fontWeight': 'bold'}
            )
    
    # Afficher le message si ce n'est pas encore 20h
    return html.Div('Report will update at 20:00')

# Lancer le serveur
if __name__ == '__main__':
    app.run(debug=True)
