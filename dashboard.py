import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px


def load_data():
    data = pd.read_csv("data.csv")
    data["timestamp"] = pd.to_datetime(data["timestamp"])
    return data


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1("Tableau de bord"),
                        html.P("Dernière mise à jour :"),
                        html.P(id="last-update"),
                        dcc.Interval(id="interval-component", interval=5 * 60 * 1000, n_intervals=0),
                    ]
                ),
            ],
            className="mt-4 mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3("Graphique des séries chronologiques"),
                        dcc.Graph(id="time-series-graph"),
                    ]
                ),
            ]
        ),
    ]
)

@app.callback(
    [Output("last-update", "children"), Output("time-series-graph", "figure")],
    [Input("interval-component", "n_intervals")],
)
def update_dashboard(n_intervals):
    data = load_data()
    last_update = data["timestamp"].max().strftime("%Y-%m-%-20 %H:%M:%S")
    fig = px.line(
    data,
    x="timestamp",
    y="value",
    title="Valeurs récupérées au fil du temps",
    labels={"timestamp": "Date et heure", "value": "Valeur"},
)

return last_update, fig
if name == "main":
app.run_server(debug=True)

