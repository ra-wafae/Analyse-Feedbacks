from pathlib import Path
import pandas as pd

def load_data():
    # Chemin absolu à partir du fichier actuel
    current_dir = Path(__file__).parent  # = dossier 'analyse'
    csv_path = current_dir / "data" / "feedbacks.csv"

    if not csv_path.exists():
        raise FileNotFoundError(f"Fichier introuvable à : {csv_path}")
    
    df = pd.read_csv(csv_path)
    return df
