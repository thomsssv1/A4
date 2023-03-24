import os
import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

def load_data():
    if not os.path.exists("data.csv"):
        with open("data.csv", "w") as f:
            f.write("timestamp,rate\n")

    data = pd.read_csv("data.csv")
    if "timestamp" not in data.columns or "rate" not in data.columns:
        raise Exception("Le fichier data.csv ne contient pas les colonnes 'timestamp' et 'rate' requises.")

    data["timestamp"] = pd.to_datetime(data["timestamp"])
    return data

def calculate_daily_metrics(data):
    today_data = data[data["timestamp"].dt.date == pd.Timestamp.now().date()]
    open_price = today_data.iloc[0]["rate"]
    close_price = today_data.iloc[-1]["rate"]
    daily_change = close_price - open_price
    daily_volatility = today_data["rate"].std()

    return {
        "open_price": open_price,
        "close_price": close_price,
        "daily_change": daily_change,
        "daily_volatility": daily_volatility
    }

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Interval(id='interval-component', interval=5*60*1000, n_intervals=0),
    html.H1("Taux de change EUR/USD"),
    dcc.Graph(id='time-series-graph'),
    html.Div(id='current-rate'),
    html.Div(id='daily-report')
])

@app.callback(
    Output('time-series-graph', 'figure'),
    Output('current-rate', 'children'),
    Output('daily-report', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_dashboard(_):
    data = load_data()
    current_rate = data.iloc[-1]["rate"]
    current_rate_text = f"Taux actuel : {current_rate}"

    fig = px.line(data, x="timestamp", y="rate", title="Taux de change EUR/USD au cours du temps")
    fig.update_xaxes(title="Date et heure")
    fig.update_yaxes(title="Taux de change")

    daily_metrics = calculate_daily_metrics(data)
    daily_report = [
        html.H3("Rapport quotidien"),
        html.P(f"Prix d'ouverture : {daily_metrics['open_price']}"),
        html.P(f"Prix de clôture : {daily_metrics['close_price']}"),
        html.P(f"Changement quotidien : {daily_metrics['daily_change']}"),
        html.P(f"Volatilité quotidienne : {daily_metrics['daily_volatility']}")
    ]

    return fig, current_rate_text, daily_report

if __name__ == "__main__":
    app.run_server(debug=True)
