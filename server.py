from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

CSV_PATH = os.path.join(os.path.dirname(__file__), "ReceiverGSR.csv")

@app.route("/latest")
def latest():
    try:
        if not os.path.exists(CSV_PATH):
            return jsonify({"error": "Fichier CSV introuvable."}), 404

        df = pd.read_csv(CSV_PATH)
        if df.empty:
            return jsonify({"error": "Le fichier CSV est vide."}), 400

        if "Timestamp" not in df.columns:
            return jsonify({"error": "Colonne 'Timestamp' manquante dans le CSV."}), 400

        value_col = None
        for col in ["GSR Value (uS)", "GSR Value", "GSR Value (V)"]:
            if col in df.columns:
                value_col = col
                break

        if not value_col:
            return jsonify({"error": "Aucune colonne de données GSR valide trouvée."}), 400

        last = df.dropna().iloc[-1]
        return jsonify({
            "timestamp": last["Timestamp"],
            "gsr": float(last[value_col])
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("🚀 Serveur Flask en ligne sur http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
