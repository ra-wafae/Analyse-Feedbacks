from flask import Flask, render_template
import pandas as pd
from pathlib import Path

app = Flask(__name__)

from pathlib import Path
import pandas as pd

def load_data():
    csv_path = Path(__file__).parent / "data" / "participation_meeting_finale.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"Fichier introuvable : {csv_path}")
    return pd.read_csv(csv_path)


@app.route('/')
def dashboard():
    df = load_data()

    # Si le fichier contient une colonne 'entree' et 'score', voici un exemple de traitement
    if 'entree' in df.columns and 'score' in df.columns:
        df['entree'] = pd.to_datetime(df['entree'], errors='coerce')
        df = df.dropna(subset=['entree'])
        df['mois'] = df['entree'].dt.to_period('M').astype(str)
        evolution = df.groupby('mois')['score'].mean()
        table_html = evolution.to_frame(name="Score moyen").to_html(classes="table table-striped", border=0)
    else:
        # Sinon on affiche simplement tout le tableau
        table_html = df.to_html(classes="table table-bordered", index=False, border=0)

    return render_template("dashboard.html", table=table_html)

if __name__ == "__main__":
    app.run(debug=True)
