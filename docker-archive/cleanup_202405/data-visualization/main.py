import dash
from dash import html

# cria a app Dash
app = dash.Dash(
    __name__,
    title="Data Visualization Service"
)

# layout simples de exemplo
app.layout = html.Div([
    html.H1("Data Visualization Service"),
    html.P("Sua plataforma de visualização de dados com Plotly Dash.")
])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050)
