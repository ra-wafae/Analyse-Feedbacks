from flask import Flask, render_template
import pandas as pd
from utils.analysis import calculate_stats, generate_wordcloud
from utils.visualizations import plot_evolution, plot_sentiment_distribution
import os

app = Flask(__name__)

# Charger les données
def load_data():
    df = pd.read_csv("data/participation_meeting_finale.csv", parse_dates=['entree'])
    df['mois'] = df['entree'].dt.to_period('M').astype(str)
    return df

@app.route('/')
def dashboard():
    df = load_data()
    
    # Calculer les indicateurs
    stats = calculate_stats(df)
    
    # Générer les visualisations
    evolution_plot = plot_evolution(df)
    sentiment_plot = plot_sentiment_distribution(df)
    wordcloud_pos = generate_wordcloud(df[df['sentiment'] == 'positif']['remarque'], "Remarques Positives")
    wordcloud_neg = generate_wordcloud(df[df['sentiment'] == 'négatif']['remarque'], "Remarques Négatives")
    
    return render_template(
        'dashboard.html',
        stats=stats,
        evolution_plot=evolution_plot,
        sentiment_plot=sentiment_plot,
        wordcloud_pos=wordcloud_pos,
        wordcloud_neg=wordcloud_neg
    )

if __name__ == '__main__':
    app.run(debug=True)