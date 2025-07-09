import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import base64
from io import BytesIO

# Charger les données
df = pd.read_csv("participation_meeting_finale_avec_sentiment.csv")
df['date'] = pd.to_datetime(df['date'])
df['mois'] = df['date'].dt.to_period('M').astype(str)

# Initialiser l'app
app = dash.Dash(__name__)
app.title = "Feedbacks Apprenants"

# Layout
app.layout = html.Div([
    html.H1("📊 Tableau de bord des feedbacks apprenants"),

    html.Label("Choisir une formation :"),
    dcc.Dropdown(
        id='formation-dropdown',
        options=[{'label': f, 'value': f} for f in df['formation'].unique()],
        value=df['formation'].unique()[0]
    ),

    dcc.Graph(id='sentiment-bar'),

    dcc.Graph(id='evolution-line'),

    html.Img(id='wordcloud-img', style={'width': '100%', 'height': '400px'}),

    html.H4("Feedbacks bruts :"),
    html.Div(id='feedback-table')
])

# Callbacks
@app.callback(
    Output('sentiment-bar', 'figure'),
    Output('evolution-line', 'figure'),
    Output('wordcloud-img', 'src'),
    Output('feedback-table', 'children'),
    Input('formation-dropdown', 'value')
)
def update_dashboard(formation):
    df_filtré = df[df['formation'] == formation]

    # Sentiment bar
    fig_sentiment = px.bar(
        df_filtré['sentiment'].value_counts().reset_index(),
        x='index', y='sentiment',
        color='index',
        labels={'index': 'Sentiment', 'sentiment': 'Nombre'},
        title="Répartition des sentiments"
    )

    # Évolution dans le temps
    feedbacks_par_mois = df_filtré.groupby('mois').size().reset_index(name='nb')
    fig_evolution = px.line(
        feedbacks_par_mois,
        x='mois', y='nb',
        markers=True,
        title="Évolution des feedbacks dans le temps"
    )

    # Wordcloud
    texte = " ".join(df_filtré['commentaire'].dropna())
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(texte)
    buffer = BytesIO()
    wordcloud.to_image().save(buffer, format="PNG")
    wordcloud_img = base64.b64encode(buffer.getvalue()).decode()
    wordcloud_src = f"data:image/png;base64,{wordcloud_img}"

    # Table des feedbacks
    table_rows = [
        html.Tr([html.Th("Date"), html.Th("Sentiment"), html.Th("Commentaire")])
    ] + [
        html.Tr([
            html.Td(row['date'].strftime("%Y-%m-%d")),
            html.Td(row['sentiment']),
            html.Td(row['commentaire'])
        ]) for _, row in df_filtré[['date', 'sentiment', 'commentaire']].head(10).iterrows()
    ]

    return fig_sentiment, fig_evolution, wordcloud_src, html.Table(table_rows, style={'width': '100%'})

# Lancer l'app
if __name__ == '__main__':
    app.run_server(debug=True)
