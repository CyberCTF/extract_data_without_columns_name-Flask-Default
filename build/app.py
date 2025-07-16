from flask import Flask, render_template, jsonify, request
import json
import os
from database import db

app = Flask(__name__, template_folder='templates', static_folder='static')

def load_metadata():
    """Load metadata from JSON file in deploy directory"""
    metadata_path = os.path.join(os.path.dirname(__file__), '..', 'deploy', 'metadata.json')
    try:
        with open(metadata_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "site": {"name": "FinTrack", "description": "Financial tracking platform for startups"},
            "navigation": {"main": [], "auth": []},
            "footer": {"links": [], "social": []},
            "challenge": {"title": "Team Member Search", "description": "Search and manage team members", "skills": [], "points": 0},
            "cta": {"label": "Access Dashboard", "link": "/lab"}
        }

@app.route('/')
def home():
    metadata = load_metadata()
    return render_template('home.html', metadata=metadata)

@app.route('/lab')
def lab():
    """Team member search dashboard"""
    metadata = load_metadata()
    search_term = request.args.get('search', '')
    
    if search_term:
        # Use the vulnerable search function
        team_members = db.search_team_members(search_term)
    else:
        # Show all team members when no search term
        team_members = db.get_all_users()
    
    return render_template('lab.html', metadata=metadata, team_members=team_members, search_term=search_term)

@app.route('/api/metadata')
def api_metadata():
    return jsonify(load_metadata())

@app.route('/api/search')
def api_search():
    """API endpoint for team member search"""
    search_term = request.args.get('q', '')
    results = db.search_team_members(search_term)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 