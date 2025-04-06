import dash
from dash import dcc, html
import plotly.graph_objs as go
from dash.dash_table import DataTable
import time
import pandas as pd
import numpy as np

# Create the Dash app
app = dash.Dash(__name__)

# Data for the graph (prices will be updated every minute)
price_data = []
timestamps = []

# Function to read the current price from the file
def read_price(file_name):
    with open(file_name, 'r') as f:
        return f.read().strip()

# Function to calculate volatility and returns (for other pairs)
def calculate_volatility(prices):
    return np.std(prices)

def calculate_return(prices):
    return (prices[-1] - prices[0]) / prices[0]

# Example pairs and their price data
currency_pairs = ['USD/JPY', 'EUR/USD', 'GBP/USD', 'USD/CHF', 'EUR/JPY']
prices_dict = {
    'USD/JPY': 'price.txt',  # file for USD/JPY
    'EUR/USD': 'price_eur_usd.txt',  # file for EUR/USD
    'GBP/USD': 'price_gbp_usd.txt',  # file for GBP/USD
    'USD/CHF': 'price_usd_chf.txt',  # file for USD/CHF
    'EUR/JPY': 'price_eur_jpy.txt',  # file for EUR/JPY
}

# Layout of the app with custom styles
app.layout = html.Div(
    children=[
        html.H1("USD/JPY Price Tracker", style={'textAlign': 'center', 'color': '#F57C00', 'fontSize': '50px'}),

        # Display the current USD/JPY price
        html.Div(id='live-update-price', style={'textAlign': 'center', 'fontSize': '24px', 'color': '#212121'}),

        dcc.Graph(id='live-update-graph'),

        dcc.Interval(
            id='interval-component',
            interval=1*60*1000,  # Update every 1 minute
            n_intervals=0
        ),

        html.Div(id='currency-prices-table', style={'textAlign': 'center', 'fontSize': '18px', 'color': '#424242', 'marginTop': '20px'})
    ],
    style={'backgroundColor': '#f0f4f8', 'padding': '20px'}
)

# Callback to update the current price
@app.callback(
    dash.dependencies.Output('live-update-price', 'children'),
    [dash.dependencies.Input('interval-component', 'n_intervals')]
)
def update_price(n):
    price = read_price('price.txt')  # Change based on file
    return f"Current USD/JPY Price: {price}"

# Callback to update the price graph
@app.callback(
    dash.dependencies.Output('live-update-graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    price = read_price('price.txt')  # Change based on file
    timestamps.append(time.strftime("%H:%M:%S"))
    price_data.append(float(price))  # Add the new price to the price data
    return {
        'data': [go.Scatter(x=timestamps, y=price_data, mode='lines+markers', line=dict(color='yellow'))],
        'layout': go.Layout(
            title='USD/JPY Price over Time',
            xaxis=dict(title='Time', showgrid=False),
            yaxis=dict(title='Price', showgrid=True),
            hovermode='closest',
            plot_bgcolor='#1c1c1c',
            paper_bgcolor='#1c1c1c',
            font=dict(family='Arial, sans-serif', size=14, color='gray')
        )
    }

# Callback to update the currency pairs report
@app.callback(
    dash.dependencies.Output('currency-prices-table', 'children'),
    [dash.dependencies.Input('interval-component', 'n_intervals')]
)
def update_currency_report(n):
    report_data = []

    for pair, file in prices_dict.items():
        price = read_price(file)
        report_data.append({
            'Currency Pair': pair,
            'Price': price,
        })

    return html.Div(
        children=[
            html.H3("Currency Prices", style={'textAlign': 'center'}),
            DataTable(
                data=report_data,
                columns=[
                    {'name': 'Currency Pair', 'id': 'Currency Pair'},
                    {'name': 'Price', 'id': 'Price'}
                ],
                style_table={'width': '80%', 'margin': 'auto'},
                style_cell={'textAlign': 'center', 'padding': '10px', 'border': '1px solid #ddd'},
                style_header={'backgroundColor': '#f0f4f8', 'fontWeight': 'bold'}
            )
        ]
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
