from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__, template_folder='templates', static_folder='static')

def load_metadata():
    """Charge les métadonnées depuis le fichier JSON dans deploy"""
    metadata_path = os.path.join(os.path.dirname(__file__), '..', 'deploy', 'metadata.json')
    try:
        with open(metadata_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "site": {"name": "CyberCTF Library", "description": "A Capture The Flag platform"},
            "navigation": {"main": [], "auth": []},
            "footer": {"links": [], "social": []},
            "challenge": {"title": "Challenge", "description": "Description", "skills": [], "points": 0},
            "cta": {"label": "Start", "link": "/"}
        }

@app.route('/')
def home():
    metadata = load_metadata()
    return render_template('home.html', metadata=metadata)

@app.route('/api/metadata')
def api_metadata():
    return jsonify(load_metadata())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 